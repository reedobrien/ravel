from urlparse import parse_qs
from repoze.bfg.chameleon_zpt import get_template
from repoze.bfg.security import authenticated_userid
from repoze.bfg.url import route_url



def index(request):
    api = get_template("ravel:templates/main.pt")
    collection =  request.context.collection 
    page = collection.find_one({'url_id' : 'home'})
    logged_in = authenticated_userid(request)
    if page:
        title = page['title']
        description = page['description']
        body = page['body']
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
        'section' : 'home',
        'title': title,
        }

def about(request):
    api = get_template("ravel:templates/main.pt")
    collection =  request.context.collection 
    page = collection.find_one({'url_id' : 'about'})
    logged_in = authenticated_userid(request)
    if page:
        title = page['title']
        description = page['description']
        body = page['body']
    else:
        page = dict(
            title = 'About ravel',
            description = "A zpug demo presentation app",
            body = '<p>Just a buggy demo hack</p>',
            url_id = 'about')
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
        'section' : 'about',
        'title': title,

        }

def article_listing(request):
    api = get_template('ravel:templates/main.pt')
    query_string = parse_qs(request.get("QUERY_STRING", None))
    batch_start = query_string.get('batch_start', 0)
    limit = query_string.get('limit', 10)
    collection = request.context.db.pages
    articles = collection.find().skip(int(batch_start)).limit(int(limit))
    return {
        'api' : api,
        'title' : "Article Listing",
        'description' : "A listing of articles",
        'logged_in' : authenticated_userid(request),
        'section' : 'articles',
        'articles' : articles,
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


