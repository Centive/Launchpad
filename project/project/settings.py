import os
import environ

root = environ.Path(__file__) - 2  # two folders back (/a/b/ - 2 = /)
env = environ.Env(DJANGO_DEBUG=(bool, False), )  # set default values and casting
environ.Env.read_env(os.environ.get('LAUNCHPAD_CONFIG_FILE'))  # reading .env file

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = root()

SECRET_KEY = env('DJANGO_SECRET_KEY')  # Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
DEBUG = env('DJANGO_DEBUG')  # False if not in os.environ
ALLOWED_HOSTS = [env('DJANGO_ALLOWED_HOSTS')]
INTERNAL_IPS = ['127.0.0.1']

CORS_ORIGIN_WHITELIST = (
    env('DJANGO_ALLOWED_HOSTS') + ':8000',
    env('DJANGO_ALLOWED_HOSTS') + ':4200',
)

CORS_URLS_REGEX = r'^/launchpad/data/.*$'
CORS_ALLOW_CREDENTIALS = True

# Application definition
INSTALLED_APPS = [
    'corsheaders',
    'accounts.apps.AccountsConfig',
    'launchpad.apps.LaunchpadConfig',
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'mathfilters',
    'crispy_forms',
    'anymail',
    'zxcvbn_password',
    'django_gravatar',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database
DATABASES = {
    'default': env.db(),
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'zxcvbn_password.ZXCVBNValidator',
        'OPTIONS': {
            'min_score': 3,
            'user_attributes': ('email')
        }
    }
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'launchpad:home'
LOGOUT_REDIRECT_URL = LOGIN_URL

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

# Session settings
# WARNING: Do not change without discussing security with peers
SESSION_COOKIE_AGE = 21600  # 6 hours, in seconds
SESSION_COOKIE_DOMAIN = '.centive.org'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = 'centag'
SESSION_COOKIE_SECURE = not DEBUG
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

# Flash Messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Crispy form settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_FAIL_SILENTLY = not DEBUG

# Anymail Settings
ANYMAIL = {
    "SENDGRID_API_KEY": env('SENDGRID_API_KEY'),
    "SENDGRID_MERGE_FIELD_FORMAT": "-{}-",
}
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = "Centive <noreply@centive.org>"