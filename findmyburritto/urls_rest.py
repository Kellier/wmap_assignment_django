from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse

from . import views, rest_view

urlpatterns = [
    url(r'^tokenlogin/$', rest_view.token_login, name='token-login'),
    url(r'^userme/$', rest_view.UserMe_R.as_view(), name='user-me'),
    url(r'^users/$', rest_view.UsersList.as_view(), name='users'),
    url(r'^user/(?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)/$', rest_view.UserOther_R.as_view(), name='user-email'),
    url(r'^user/(?P<uid>\d+)/$', rest_view.UserOther_R.as_view(), name='user-username'),
    url(r'^updateposition/$', rest_view.UpdatePosition.as_view(), name='update-position'),
    url(r'^getamenities/$', rest_view.get_burritos, name='get-burritos'),
]