from django.conf.urls import include, url
from .import views

urlpatterns = [
    url(r'^vcards/', views.vcard, name='vcard_index'),
]