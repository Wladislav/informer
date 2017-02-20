from django.conf.urls import include, url
from .import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^accounts/register/$', views.newRegistratonView.as_view(), name='registration_register'),
    url(r'^',include('password_reset.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url('^', include('django.contrib.auth.urls')),
    url(r'^accounts/profile/$', views.user_profile, name='user_profile'),
    #url(r'^accounts/profile/(?P<pk>[\d]+)/$', views.user_profile, name="user_profile"),
]







