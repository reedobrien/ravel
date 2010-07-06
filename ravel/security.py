## for security stuff

#needs a user in the db like so
"""
user = {'username': 'admin', 
        'last_login': [], 
        'groups': ['group:editors', 'group:admins'], 
        'password': '58acb7acccce58ffa8b953b12b5a7702bd42dae441c1ad85057fa70b', 
        'email': 'info@koansys.com'}
"""



def groupfinder(userid, request):
    try:
        user = request.root.db['users'].find({'username' : userid}).next()
    except StopIteration:
        user = None
    if user:
        return user['groups']
    
