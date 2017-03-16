from django.conf.urls import url
from django.contrib import admin
from .views import generate_csv, subscribe_detail

admin.autodiscover()

urlpatterns = [
    #url(r'^admin/newsletter/subscription/download/csv/$', generate_csv, name='download_csv'),
    #url(r'^$', subscribe_detail, name='subscribe_detail'), #Подписка на главной странице
]

