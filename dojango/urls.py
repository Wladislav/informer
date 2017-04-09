from django import VERSION as django_version
from django.conf.urls import url
from django.conf import settings
from .import views 
from dojango.util import media
   
urlpatterns = [
    url(r'^test/$', views.test, name='dojango-test'),
    url(r'^test/countries/$', views.test_countries),
    url(r'^test/states/$', views.test_states),
    # Note: define accessible objects in DOJANGO_DATAGRID_ACCESS setting
    url(r'^datagrid-list/(?P<app_name>.+)/(?P<model_name>.+)/$', views.datagrid_list, name="dojango-datagrid-list"),
]

if settings.DEBUG:
    urlpatterns += media.url_patterns
