DEBUG = False

# modifier la clef secrète
SECRET_KEY = '#xinfvd=+#^del$@he^ms46$$2mrf!)+4i6icn62fx&t+4p2^a'

# exemple de configuration de bases de données

# PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'simonetti',
        'HOST': 'localhost',
        'PASSWORD': 'simonetti',
        'PORT': '5432',
        'USER': 'simonetti',
    }
}

# SqlLite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ALLOWED_HOSTS = ["url_backend", "url_frontend"]

# configuration Email smtp
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'email@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587
