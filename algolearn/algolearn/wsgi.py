import os
from django.core.wsgi import get_wsgi_application
from whitenoise import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "algolearn.settings")

application = get_wsgi_application()
application = django.DjangoWhiteNoise(application)