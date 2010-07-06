from hashlib import sha224

from webob.exc import HTTPFound

from repoze.bfg.chameleon_zpt import get_template
from repoze.bfg.security import remember
from repoze.bfg.security import forget
from repoze.bfg.url import route_url


def login(request):
    api = get_template("ravel:templates/main.pt")
    login_url = route_url('login', request)
    referrer = request.url
    if referrer == login_url:
        referrer = '/'
    came_from = request.params.get('came_from', referrer)
    message = login = password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        try:
            user = request.root.db['users'].find({'username': login}).next()
        except StopIteration:
            user = None
        if user:
            if sha224(password).hexdigest() == user['password']:
                headers = remember(request, login)
                return HTTPFound(location=came_from,
                                 headers=headers)
        message = 'Login failed'
    return dict(
        api = api,
        came_from = came_from,
        login = login,
        message = message,
        password = password,
        section = 'login',
        title = 'ravel | Log in',
        url = request.application_url + '/login',
        )

def logout(request):
    headers = forget(request)
    return HTTPFound(location=route_url('home', request),
                     headers = headers)
