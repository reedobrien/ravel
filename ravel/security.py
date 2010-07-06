## for security stuff
import pymongo

from repoze.bfg.settings import get_settings

def groupfinder(userid, request):
    settings = get_settings()
    db = pymongo.Connection.from_uri(
        uri=settings['db_uri'])[settings['db_name']]
    user = None
    user = db['users'].find({'username' : userid}).next()
    print user
    if user:
        return user['groups']
    
