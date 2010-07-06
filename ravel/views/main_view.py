from repoze.bfg.chameleon_zpt import get_template
from repoze.bfg.security import authenticated_userid
from repoze.bfg.url import route_url

from lumin import insert_doc

def index(request):
    api = get_template("ravel:templates/main.pt")
    collection =  request.context.collection 
    page = collection.find_one({'url_id' : 'home'})
    logged_in = authenticated_userid(request)
    if page:
        title = page['title']
        description = page['description']
        body = page['body']
        route_url('page_edit', request, page_id="home"),
    else:
        page = dict(
            title = 'Home',
            description = "A zpug demo presentation app",
            body = '<p>Edit me again please</p>',
            url_id = 'home')
        collection.save(page)
        title = page['title']
        description = page['description']
        body = page['body']
        
    return {
        'api' : api,
        'body' : body,
        'description': description,
        'edit_url' :  route_url('page_edit', request, page_id="home"),
        'logged_in' : logged_in,
        'title': title,

        }


def not_implemented(request):
    api = get_template('ravel:templates/main.pt')
    path = request.get('PATH_INFO').strip('/')
    logged_in = authenticated_userid(request)
    return {
        'api' : api,
        'description' : "An unimplemented page",
        'logged_in' : logged_in,
        'path': path,
        'title':'Not Implemented',
        }
