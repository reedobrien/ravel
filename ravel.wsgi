## for mod_wsgi

import os
from repoze.bfg.paster import get_app

dir = os.path.dirname(__file__)
inipath = os.path.join(dir, 'ravel.ini')

application = get_app(inipath, 'main')
