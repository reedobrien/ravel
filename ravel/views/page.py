import logging

from webob.exc import HTTPFound

from pyramid.chameleon_zpt import get_template
from pyramid.exceptions import NotFound
from pyramid.security import authenticated_userid
from pyramid.url import route_url

from deform import Form
from deform import ValidationFailure
from deform import widget

from lumin import insert_doc

from ravel.models.comment import Comment

logging.basicConfig(level=logging.INFO)

def page_view(request):
    page_id = request.matchdict['page_id']
    page = request.context.page
    if not page:
        ## TODO: setup notfound view
        raise NotFound("No such page {0}".format(page_id))
    logged_in = authenticated_userid(request)
    api = get_template('ravel:templates/main.pt')
    commentschema = Comment()
    commentform = Form(commentschema,
                       action=route_url('comment_add', 
                                        request,
                                        page_id=page_id),
                       buttons=('submit',),
                       use_ajax=True)
    commentform['comment'].widget = widget.TextAreaWidget(rows=10, cols=60)
    print page.get('comments', None)
    return {
        'api' : api,
        'description' : page['description'],
        'edit_url' :  route_url('page_edit', request, page_id=page_id),
        'logged_in' : logged_in,
        'title' : page['title'],
        'body' : page['body'],
        'commentform' : commentform.render(),
        'comments' : page.get('comments', None)
        }
   

def page_add(request):
    logged_in = authenticated_userid(request)
    api = get_template('ravel:templates/main.pt')
    schema = request.context.schema
    form = Form(schema, buttons=('submit',))
    form['body'].widget = widget.TextAreaWidget(rows=10, cols=60)
    if request.method == "POST":
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except ValidationFailure, e:
            return {
                'api'   : api,
                'description' : 'Add page',
                'form': e.render(),
                'logged_in' : logged_in,
                'title' : 'Edit page',
                }
        title_or_id = appstruct['title']
        url_id = insert_doc(request.context.collection, appstruct, title_or_id)
        oid = request.context.collection.save(appstruct, safe=True)
        logging.info("page_edit saved {0}".format(oid))
        return HTTPFound(location=route_url('page_view', request, page_id=url_id))
    return {
        'api'   : api,
        'description' : 'Add page',
        'form': form.render(),
        'logged_in' : logged_in,
        'title' : 'Add page',
        }
    

def page_edit(request):
    page_id = request.matchdict['page_id']
    page = request.context.page
    if not page:
        ## TODO: setup notfound view
        raise NotFound("No such part {0}".format(page_id))
    logged_in = authenticated_userid(request)
    api = get_template('ravel:templates/main.pt')
    schema = request.context.schema
    form = Form(schema, buttons=('submit',))
    form['body'].widget = widget.TextAreaWidget(rows=10, cols=60)
    if request.method == "POST":
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except ValidationFailure, e:
            return {
                'api'   : api,
                'description' : 'Edit ' + page['title'],
                'form': e.render(),
                'logged_in' : logged_in,
                'title' : 'Edit ' + page['title'],
                }
        appstruct['_id'] = page['_id']
        appstruct['url_id'] = page_id
        oid = request.context.collection.save(appstruct, safe=True)
        logging.info("page_edit saved {0}".format(oid))
        return HTTPFound(location=route_url('page_view', request, page_id=page_id))
        
    return {
        'api' : api,
        'description' : 'Edit ' + page['title'],
        'form' : form.render(page),
        'logged_in' : logged_in,
        'title' : "Edit " + page['title'],
        }
