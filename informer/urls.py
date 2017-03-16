from django.conf.urls import include, url
from .import views
from password_reset import views as password_reset_views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^accounts/register/$', views.newRegistratonView.as_view(), name='registration_register'),
    url(r'^reset/done/$', password_reset_views.reset_done, name='recovery_done'),
    url(r'^reset/(?P<token>[\w:-]+)/$', views.reset, name='password_reset_reset'),
    url(r'^',include('password_reset.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url('^', include('django.contrib.auth.urls')),
    url(r'^accounts/profile/$', views.user_profile, name='user_profile'),
    url(r'', include('subscribe.urls')),
    url(r'^newsletter/', include('newsletter.urls')),
    #url(r'^', include('debug_toolbar_htmltidy.urls')),
]








