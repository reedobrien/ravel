import logging
import smtplib

import colander
from colander import SchemaNode
from colander import String

from lumin import RootFactory

from repoze.bfg.security import Allow
from repoze.bfg.security import Everyone
from repoze.bfg.exceptions import NotFound

logging.basicConfig(level=logging.INFO)


class PageSchema(colander.MappingSchema):
    title = SchemaNode(String(),
                       title='Page title',
                       description='The title of the page',
                       )
    description  = SchemaNode(String(),
                              title='A short description', 
                              description='Keep it under 60 characters or so',
                              missing = u'',
                              validator=colander.Length(max=79)
                              )
    body = colander.SchemaNode(colander.String(),
                               description='Tell the world',
                               missing = u'')



class Page(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'group:users', ('add', 'edit')),
        (Allow, 'group:admins', ('add', 'edit', 'delete')),
        ]
    ## set collection to parent as well in case we ever want to use traversal
    ## say for a taxonomy or something
    __parent__ = __collection__ = 'pages'


    def __init__(self, request, root_factory=RootFactory):
        self.__dict__.update(root_factory(request).__dict__)
        self.collection = self.db[self.__collection__]
        self.environ = request.environ
        self.page_id = request.matchdict.get('page_id')
        self.request = request
        if self.page_id:
            cursor = self.collection.find(
                {u'url_id' : self.page_id})
            try:
                self.page = cursor.next()
            except StopIteration:
                self.page = None
            if cursor.count()>1:
                NotFound("There should never be more than ONE. However " 
                         "there are {0} results for {1}. This Error has "
                         "been logged and the administrators have been "
                         "notified".format(
                        cursor.count(), self.page_id))
                logging.critical("There should never be more than ONE. However " 
                                 "there are {0} results for {1}".format(
                        cursor.count(), self.page_id))
                ## TODO: move this to a utility finction somehwere and mail it
                ## TODO: to all users with the admin or maintenance role 
                s = smtplib.SMTP('localhost')
                msg = """Subject: Ravel DB Error
From: Ravel
To: You fix me

There should never be more than ONE. However there are {0} results for {1}. 
Please fix this in {2} {3}""".format(cursor.count(), self.page_id, self.db, self.collection)
                s.send_mail('info@koansys.com', 'info@koansys.com', msg)
        else:
            self.page = None
        self.schema = PageSchema()
        #add metadata somwhere
                
