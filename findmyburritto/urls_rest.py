from django.conf.urls import url

from . import rest_view

urlpatterns = [
    url(r'^tokenlogin/$', rest_view.token_login, name='token-login'),
    url(r'^me/$', rest_view.UserMain_R.as_view(), name='user-me'),
    url(r'^users/$', rest_view.UsersList.as_view(), name='users'),
    url(r'^user/(?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)/$', rest_view.UserRegular_R.as_view(), name='user-email'),
    url(r'^user/(?P<uid>\d+)/$', rest_view.UserRegular_R.as_view(), name='user-username'),
    url(r'^updateposition/$', rest_view.UpdatePosition.as_view(), name='update-position'),
]