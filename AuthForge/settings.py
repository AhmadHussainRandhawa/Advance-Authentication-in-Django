from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'unsafe'),
    ALLOWED_HOSTS=(list, []),
    DATABASE_URL=(str, f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),  # ✅ fallback
)

environ.Env.read_env(BASE_DIR / '.env')

# use env variables now
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # My apps
    'core_auth',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AuthForge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'AuthForge.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': env.db(default=env('DATABASE_URL'))
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# AUTHENTICATION

AUTH_USER_MODEL = 'core_auth.User'

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

LOGIN_URL = 'core_auth:login'

LOGIN_REDIRECT_URL = '/'  # or a dashboard path

LOGOUT_REDIRECT_URL = 'core_auth:login'

# The number of seconds a password reset link is valid for (default: 3 days).
PASSWORD_RESET_TIMEOUT = 60 * 60 * 24 * 3

# the first hasher in this list is the preferred algorithm.  any
# password using different algorithms will be converted automatically
# upon login

AUTH_PASSWORD_VALIDATORS = []

# For password reset email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@authforge.dev'

#SESSIONS

# Cache to store session data if using the cache session backend.
SESSION_CACHE_ALIAS = "default"
# Cookie name. This can be whatever you want.
SESSION_COOKIE_NAME = "sessionid"
# Age of cookie, in seconds (default: 2 weeks).
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
# A string like "example.com", or None for standard domain cookie.
SESSION_COOKIE_DOMAIN = None
# Whether the session cookie should be secure (https:// only).
SESSION_COOKIE_SECURE = False
# The path of the session cookie.
SESSION_COOKIE_PATH = "/"
# Whether to use the HttpOnly flag.
SESSION_COOKIE_HTTPONLY = True
# Whether to set the flag restricting cookie leaks on cross-site requests.
# This can be 'Lax', 'Strict', 'None', or False to disable the flag.
SESSION_COOKIE_SAMESITE = "Lax"
# Whether to save the session data on every request.
SESSION_SAVE_EVERY_REQUEST = False
# Whether a user's session cookie expires when the web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# The module to store session data
SESSION_ENGINE = "django.contrib.sessions.backends.db"
# Directory to store session files if using the file session module. If None,
# the backend will use a sensible default.
SESSION_FILE_PATH = None
# class to serialize session data
SESSION_SERIALIZER = "django.contrib.sessions.serializers.JSONSerializer"
