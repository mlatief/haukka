import os
# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = BASE_DIR + '/haukka-ui'
STATIC_PREFIX = ''

DATABASE_URI = os.environ.get('DATABASE_URL', "postgresql:///haukka?connect_timeout=5")
TEST_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', "postgresql:///haukka_test?connect_timeout=5")

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True
# Secret key for signing cookies
SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')
# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY', 'secret')

# Force to False so that app tearDown is called even in Debug mode
PRESERVE_CONTEXT_ON_EXCEPTION = False

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2
