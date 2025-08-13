import os
from pathlib import Path
import environ
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    SECRET_KEY=(str, "django-insecure-dummy-key-for-builds-and-dev-only"),
    DATABASE_URL=(str, "sqlite:///dummy.db"),
    ALLOWED_HOSTS=(str, "*"),
    CSRF_TRUSTED_ORIGINS=(str, "https://*, http://*"),
    USE_X_FORWARDED_HOST=(bool, False),
    WAGTAIL_SITE_NAME=(str, "Wagtail Starter Kit"),
    WAGTAILADMIN_BASE_URL=(str, "http://localhost:8000"),
)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")


INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Wagtail apps
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    # Optional Wagtail apps
    "wagtail.contrib.routable_page",
    "wagtail.contrib.settings",
    "wagtail.contrib.search_promotions",
    # Third-party apps
    "taggit",
    "modelcluster",
    # SEO
    "wagtailseo",
    # Caching
    "wagtailcache",
    # Forms
    "wagtail_flexible_forms",
    "django_htmx",
    # Frontend integration
    "webpack_boilerplate",
    "turbo_helper",
    # Our apps
    "apps.core",
    "apps.home",
    "apps.frontend",
    "apps.blocks",
    "apps.navigation.apps.NavigationConfig",
    "apps.settings",
    "apps.search",
    "apps.forms",
    "apps.snippets",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "turbo_helper.middleware.TurboMiddleware",
]

# if not DEBUG:
#     MIDDLEWARE.insert(1, "wagtailcache.cache.UpdateCacheMiddleware")
#     MIDDLEWARE.append("wagtailcache.cache.FetchFromCacheMiddleware")

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default=env("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "apps/frontend/build"),
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Wagtail settings
WAGTAIL_SITE_NAME = env("WAGTAIL_SITE_NAME")
WAGTAILADMIN_BASE_URL = env("WAGTAILADMIN_BASE_URL")

# Disable password validators for development
AUTH_PASSWORD_VALIDATORS = []

# SECURITY WARNING: define the correct hosts in production!
# This should be set to your domain or IP address in production
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS").split(",")
USE_X_FORWARDED_HOST = env("USE_X_FORWARDED_HOST")

# Increase the maximum number of fields for complex page models
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# Wagtail Cache settings
WAGTAIL_CACHE = True
WAGTAIL_CACHE_BACKEND = "default"

# Cache settings
# if DEBUG:
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}
# else:
#     CACHES = {
#         "default": {
#             "BACKEND": "django_redis.cache.RedisCache",
#             "LOCATION": "redis://127.0.0.1:6379/1",
#             "OPTIONS": {
#                 "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             },
#         }
#     }

# Webpack loader settings
WEBPACK_LOADER = {
    "MANIFEST_FILE": os.path.join(BASE_DIR, "apps/frontend/build/manifest.json"),
}
