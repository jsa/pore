import logging
import os

from google.appengine.api.app_identity.app_identity import get_application_id

try:
    appid = get_application_id()
except AttributeError:
    appid = None

IS_PROD = not os.environ.get('SERVER_SOFTWARE', "").startswith("Development/") \
          and appid == 'pic-repo'

DEBUG = TEMPLATE_DEBUG = not IS_PROD

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'GMT'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = USE_L10N = False

USE_TZ = True

if IS_PROD:
    MEDIA_VERSION = hash(os.environ.get('CURRENT_VERSION_ID')) % 10000
else:
    from random import randint
    MEDIA_VERSION = randint(1, 9999)

MEDIA_URL = "/a/%d/" % MEDIA_VERSION

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
)

if IS_PROD:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
    )

ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'gaelib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.media',
    'repo.context_processors.base_url',
    'repo.context_processors.settings',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'repo.gallery',
    'repo.photo',
)


try:
    from secrets import *
except ImportError, e:
    logging.exception(e)
    raise Exception, "Please create `secrets.py' with (at least) SECRET_KEY"
