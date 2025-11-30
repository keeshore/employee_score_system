from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-z7bf=*p_cte(l6g#0ka2w-qlsq)t@nj*rjagv%*8q+f+f86qam'

DEBUG = False

ALLOWED_HOSTS = ["*"]   # for dev, allow all. Important for ngrok & hosting.


# --------------------------------------------------------
# INSTALLED_APPS
# --------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',   # MUST COME BEFORE core
    'core',
]


# --------------------------------------------------------
# MIDDLEWARE (CORS must be at top)
# --------------------------------------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',    # Must be very first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Allow all origins for development
CORS_ALLOW_ALL_ORIGINS = True


# --------------------------------------------------------
# ZOHO API KEY (KEEP ONE)
# --------------------------------------------------------
API_KEY_FOR_ZOHO = "change_this_to_a_secret_value"


ROOT_URLCONF = 'employeescore.urls'


# --------------------------------------------------------
# TEMPLATES
# --------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],   # root template folder
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


WSGI_APPLICATION = 'employeescore.wsgi.application'


# --------------------------------------------------------
# DATABASE
# --------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# --------------------------------------------------------
# AUTH PASSWORD VALIDATORS
# --------------------------------------------------------
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


# --------------------------------------------------------
# LANGUAGE & TIMEZONE
# --------------------------------------------------------
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True


# --------------------------------------------------------
# STATIC FILES
# --------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]


# --------------------------------------------------------
# DEFAULT PRIMARY KEY
# --------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
