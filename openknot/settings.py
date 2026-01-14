from pathlib import Path
import os
import logging

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY: read secret key from env in production
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-fallback-key-for-local-dev-only"  
)

# DEBUG: set via env var ("True"/"False")
DEBUG = os.environ.get("DEBUG", "False").lower() in ("1", "true", "yes")

# ALLOWED_HOSTS: comma-separated env value or sensible defaults for local + render
_default_hosts = "127.0.0.1,localhost,housing-model-5.onrender.com,mishraankit.com.np"
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", _default_hosts).split(",") if h.strip()]

# If Render (or similar) sets RENDER_EXTERNAL_HOSTNAME, append it
render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_host and render_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(render_host)

# CSRF_TRUSTED_ORIGINS: allow explicit override or derive from ALLOWED_HOSTS
_csrf_env = os.environ.get("CSRF_TRUSTED_ORIGINS")
if _csrf_env:
    CSRF_TRUSTED_ORIGINS = [u.strip() for u in _csrf_env.split(",") if u.strip()]
else:
    CSRF_TRUSTED_ORIGINS = []
    for host in ALLOWED_HOSTS:
        # avoid localhost/127.* entries; allow only https origins for production hosts
        if host and not (host.startswith("127.") or host.startswith("localhost")):
            CSRF_TRUSTED_ORIGINS.append(f"https://{host}")

# Application definition
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'members',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'openknot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

ASGI_APPLICATION = 'openknot.asgi.application'

# Database
# Keep sqlite as default for local dev; override with DATABASE_URL in production if desired.
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DJANGO_DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DJANGO_DB_NAME', BASE_DIR / 'db.sqlite3'),
    }
}

# If you prefer to use DATABASE_URL (Postgres) in production, uncomment below and install dj-database-url:
# import dj_database_url
# DATABASES['default'] = dj_database_url.config(default=os.environ.get('DATABASE_URL'))

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# single source-of-truth for staticfiles storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings for production (apply only when DEBUG is False)
if not DEBUG:
    # When behind a proxy (Render), honor X-Forwarded-Proto header
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Redirect all HTTP to HTTPS
    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True").lower() in ("1", "true", "yes")

    # Cookies secure
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # HSTS - only enable after you confirm HTTPS is working
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", 60))  # start small, increase later
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get("SECURE_HSTS_INCLUDE_SUBDOMAINS", "True").lower() in ("1", "true", "yes")
    SECURE_HSTS_PRELOAD = os.environ.get("SECURE_HSTS_PRELOAD", "False").lower() in ("1", "true", "yes")

# Logging (basic)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler',},
    },
    'root': {
        'handlers': ['console'],
        'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
    },
}
logging.getLogger().info("Django settings loaded. DEBUG=%s ALLOWED_HOSTS=%s", DEBUG, ALLOWED_HOSTS)
