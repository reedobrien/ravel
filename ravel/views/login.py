from datetime import datetime
from hashlib import sha224

from webob.exc import HTTPFound

from pyramid.chameleon_zpt import get_template
from pyramid.security import authenticated_userid
from pyramid.security import remember
from pyramid.security import forget
from pyramid.url import route_url


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
                
                request.root.db.users.update({"_id" : user['_id']}, 
                                             {"$set" : {'last_login' : datetime.now() }})
                return HTTPFound(location=came_from,
                                 headers=headers)
        message = 'Login failed'
    return dict(
        api = api,
        came_from = came_from,
        login = login,
        logged_in = authenticated_userid(request),
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
