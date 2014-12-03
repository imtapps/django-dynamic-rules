# app lives in a directory above our example
# project so we need to make sure it is findable on our path.
import sys
from os.path import abspath, dirname, join
parent = abspath(dirname(__file__))
grandparent = abspath(join(parent, '..'))
for path in (grandparent, parent):
    if path not in sys.path:
        sys.path.insert(0, path)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'example.db',
    }
}

STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    abspath(join(parent, 'templates')),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',

    'djadmin_ext',

    'dynamic_rules',
    'sample',
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

try:
    import south
    INSTALLED_APPS = ('south', ) + INSTALLED_APPS
    SOUTH_TESTS_MIGRATE = False
except ImportError:
    pass

CACHE_EMPTY_QUERYSETS = True
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}
