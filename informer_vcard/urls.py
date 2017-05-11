from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^vcards/$', views.vcard_list, name='vcard_index'),
    url(r'^vcards/vcard_list.json/$', views.vcard_list, name='vcard_index'),
    url(r'^vcards/add/$', views.vcard_add_copy_change, name='vcard_add'),
    url(r'^vcards/[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}/change/$', views.vcard_add_copy_change, name='vcard_change'),
]