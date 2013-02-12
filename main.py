import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

def fix_paths():
    import sys
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
    LIB_DIRS = [os.path.join(PROJECT_DIR, 'lib')]
    LIB_DIRS += filter(lambda f: os.path.isdir(f) or f.endswith('.zip'),
                       [os.path.join(LIB_DIRS[0], f) for f in os.listdir(LIB_DIRS[0])])
    sys.path = LIB_DIRS + sys.path

def patch_django():
    # We don't want no stinking AnonymousUsers (overwrite class)
    import django.contrib.auth.models
    django.contrib.auth.models.AnonymousUser = lambda: None

fix_paths()
patch_django()

import django.core.handlers.wsgi
app = django.core.handlers.wsgi.WSGIHandler()
