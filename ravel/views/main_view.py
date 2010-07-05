from repoze.bfg.chameleon_zpt import get_template

def index(request):
    api = get_template("ravel:templates/main.pt")
    description = "A zpug demo presentation app"
    return {
        'api' : api,
        'description': description,
        'logged_in' : request.context.logged_in,
        'title':'ravel',
        }


def not_implemented(request):
    api = get_template('ravel:templates/main.pt')
    path = request.get('PATH_INFO').strip('/')
    return {
        'api' : api,
        'description' : "An unimplemented page",
        'logged_in' : request.context.logged_in,
        'path': path,
        'title':'Not Implemented',
        }
