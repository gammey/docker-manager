"""dockerManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from dockerManager.lib import views as docker_views
from dockerManager import views as views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^docker/list$', docker_views.nodelist),
    url(r'^docker/container/detail$', docker_views.containerDetailsList),
    url(r'^docker/image/detail$', docker_views.imagesDetailsList),
    url(r'^docker/service/(\S+)/$', docker_views.servicesDetailsList),
    url(r'^container/(\S+)/(\S+)/(\S+)/$', docker_views.containerControl),
    url(r'^image/(\S+)/(\S+)/(\S+)/$', docker_views.imageControl),
    url(r'^service/update/(\S+)/(\S+)/replicas/(\d+)/$', docker_views.updateReplicas),
    url(r'^service/update/(\S+)/(\S+)/images/(\S+)/$', docker_views.updateImages),
    url(r'^swarm/services/ps/(\S+)/', docker_views.swarmServicesProcessList),
    url(r'^$', views.index),
]
