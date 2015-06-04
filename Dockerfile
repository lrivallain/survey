#
# build:
#   docker build --rm -t templateName .
# prepare:
#   dockercmd='docker run --rm -i -t -e "DJANGO_SECRET_KEY="A_SECRET_KEY" -v "/docker/data/survey/db/:/data/proj/db" -v "/docker/data/survey:/data/proj/survey" -P -t templateName'
# init:
#   $dockercmd python manage.py makemigrations
#   $dockercmd python manage.py migrate
#   $dockercmd python manage.py createsuperuser
# run:
#   $dockercmd
#

# based on last ubuntu
FROM ubuntu:latest

# requirements
RUN apt-get update -qq && \
    apt-get install python-pip python-dev build-essential -qqy && \
    pip install django uwsgi

# start project
RUN mkdir /data/ && \
    cd /data/ && \
    django-admin startproject proj

# folder for sqlite db
RUN mkdir /data/proj/db/ && \
    sed -i "s/db\.sqlite3/db\/db\.sqlite3/g" /data/proj/proj/settings.py

# salt will be set by -e option on docker run
RUN sed -i "s/SECRET_KEY.*/SECRET_KEY=os.environ['DJANGO_SECRET_KEY']/g" /data/proj/proj/settings.py

# add the auto add apps tric to the settings.py
RUN echo "" >> /data/proj/proj/settings.py && \
    echo "# Auto add apps" >> /data/proj/proj/settings.py && \
    echo "CUSTOM_INSTALLED_APPS=()" >> /data/proj/proj/settings.py && \
    echo "for name in os.listdir(BASE_DIR):" >> /data/proj/proj/settings.py && \
    echo "    if os.path.isdir(name) and name not in ['proj', 'db']:" >> /data/proj/proj/settings.py && \
    echo "        CUSTOM_INSTALLED_APPS=CUSTOM_INSTALLED_APPS+(str(name),)" >> /data/proj/proj/settings.py && \
    echo "INSTALLED_APPS=INSTALLED_APPS+CUSTOM_INSTALLED_APPS" >> /data/proj/proj/settings.py

# templates folder
RUN echo "" >> /data/proj/proj/settings.py && \
    echo "# Templates" >> /data/proj/proj/settings.py && \
    echo "TEMPLATE_DIRS = (" >> /data/proj/proj/settings.py && \
    echo "    os.path.join(os.path.dirname(__file__),'../templates')," >> /data/proj/proj/settings.py && \
    echo ")" >> /data/proj/proj/settings.py

# static files
RUN echo "" >> /data/proj/proj/settings.py && \
    echo "# Static files" >> /data/proj/proj/settings.py && \
    echo "STATIC_URL = \"/static/\"" >> /data/proj/proj/settings.py && \
    echo "STATIC_ROOT = \"/tmp/django_static/\"" >> /data/proj/proj/settings.py

RUN echo "" >> /data/proj/proj/urls.py && \
    echo "# static files" >> /data/proj/proj/urls.py && \
    echo "from django.conf import settings" >> /data/proj/proj/urls.py && \
    echo "from django.conf.urls.static import static" >> /data/proj/proj/urls.py && \
    echo "urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) " >> /data/proj/proj/urls.py

# app urls settings
RUN echo "" >> /data/proj/proj/urls.py && \
    echo "# import apps urls" >> /data/proj/proj/urls.py && \
    echo "import importlib" >> /data/proj/proj/urls.py && \
    echo "from django.conf import settings" >> /data/proj/proj/urls.py && \
    echo "for app in settings.CUSTOM_INSTALLED_APPS:" >> /data/proj/proj/urls.py && \
    echo "    apppaterns = importlib.import_module(\"%s.urls\" % app).urlpatterns" >> /data/proj/proj/urls.py && \
    echo "    urlpatterns += apppaterns" >> /data/proj/proj/urls.py

# default configuration for uwsgi
RUN echo "[uwsgi]" >> /data/proj/uwsgi.init && \
    echo "pp=/data/proj" >> /data/proj/uwsgi.init && \
    echo "chdir=/data/proj" >> /data/proj/uwsgi.init && \
    echo "module=proj.wsgi:application" >> /data/proj/uwsgi.init && \
    echo "master=True" >> /data/proj/uwsgi.init && \
    echo "pidfile=/tmp/project-master.pid" >> /data/proj/uwsgi.init && \
    echo "vacuum=True" >> /data/proj/uwsgi.init && \
    echo "max-requests=5000" >> /data/proj/uwsgi.init && \
    echo "http=:8001" >> /data/proj/uwsgi.init

# run script
RUN echo "#!/bin/bash" >> /data/proj/runner.sh && \
    echo "python manage.py collectstatic --noinput" >> /data/proj/runner.sh && \
    echo "/usr/local/bin/uwsgi --ini /data/proj/uwsgi.init" >> /data/proj/runner.sh && \
    chmod +x /data/proj/runner.sh

# run and expose
WORKDIR /data/proj/
EXPOSE 8001
CMD ["/data/proj/runner.sh"]