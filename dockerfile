FROM centos
ENV PROJECTNAME dockerManager
ENV STATIC_PATH static

RUN yum install epel-release.noarch -y
RUN yum install python-pip gcc gcc++ python-devel.x86_64 mysql-devel -y
RUN python -m pip install "django<2"
RUN pip install uwsgi
RUN pip install requests docker

RUN mkdir /opt/django/
ADD django.tar.gz /opt/django/

ENTRYPOINT uwsgi --http 0.0.0.0:8001 --file /opt/django/$PROJECTNAME/wsgi.py --chdir /opt/django/ --static-map=/static=$STATIC_PATH
