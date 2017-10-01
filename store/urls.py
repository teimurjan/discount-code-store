from django.conf.urls import url

from store.utils.constants import LOGIN_URL_NAME, INDEX_URL_NAME, LOGOUT_URL_NAME, USERS_URL_NAME, PRODUCTS_URL_NAME, \
  FIND_USERS_URL_NAME
from store.views import IndexView, LoginView, LogoutView, UsersView, ProductsView, FindUserView

urlpatterns = [
  url(r'^$', IndexView.as_view(), name=INDEX_URL_NAME),
  url(r'^login/$', LoginView.as_view(), name=LOGIN_URL_NAME),
  url(r'^logout/$', LogoutView.as_view(), name=LOGOUT_URL_NAME),
  url(r'^users/$', UsersView.as_view(), name=USERS_URL_NAME),
  url(r'^products/$', ProductsView.as_view(), name=PRODUCTS_URL_NAME),
  url(r'^find_users/$', FindUserView.as_view(), name=FIND_USERS_URL_NAME),
]
