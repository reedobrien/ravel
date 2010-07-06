from repoze.bfg.chameleon_zpt import get_template
from repoze.bfg.security import authenticated_userid


def index(request):
    api = get_template("ravel:templates/main.pt")
    description = "A zpug demo presentation app"
    logged_in = authenticated_userid(request)
    print logged_in
    return {
        'api' : api,
        'description': description,
        'logged_in' : logged_in,
        'title': 'ravel',
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
