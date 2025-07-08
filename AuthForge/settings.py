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

    # 2FA and OTP
    'django_otp',
    'django_otp.plugins.otp_totp',     # TOTP (Google Authenticator, etc.)
    'django_otp.plugins.otp_static',   # Backup codes
    'django_otp.plugins.otp_email',    # if you want email capability.

    'two_factor',                      # Main 2FA integration
    'two_factor.plugins.phonenumber',  # Optional: for SMS if needed later
    'two_factor.plugins.email',        # if you want email capability.

    # libraries
    'widget_tweaks'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
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

LOGIN_URL = 'two_factor:login'

LOGIN_REDIRECT_URL = 'two_factor:profile'

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
