from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^vcards/$', views.vcard_list, name='vcard_index'),
    url(r'^vcards/vcard_list.json/$', views.vcard_list, name='vcard_index'),
    url(r'^vcards/add/$', views.vcard_change, name='vcard_add'),
    url(r'^vcards/[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}/change/$', views.vcard_change, name='vcard_change'),
    url(r'^vcards/[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}/change/vcard_adress.json$', views.vcard_change, name='vcard_change'),
    url(r'^vcards/[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}/change/vcard_phones.json$', views.vcard_change, name='vcard_change'),
    url(r'^vcards/[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}/change/vcard_emails.json$', views.vcard_change, name='vcard_change'),
    url(r'^vcards/[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}/change/vcard_social.json$', views.vcard_change, name='vcard_change'),
    url(r'^vcards/[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}/change/vcard_messeng.json$', views.vcard_change, name='vcard_change'),
    url(r'^vcards/[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}/change/vcard_hobby.json$', views.vcard_change, name='vcard_change'),
    url(r'^vcards/[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}/change/vcard_interest.json$', views.vcard_change, name='vcard_change'),
    url(r'^vcards/[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}/change/vcard_expertise.json$', views.vcard_change, name='vcard_change'),
]