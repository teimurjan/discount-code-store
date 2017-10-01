from django.contrib.auth import authenticate, logout
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from store.utils.constants import ERRORS_KEY, USERNAME_KEY, PASSWORD_KEY, AUTH_KEY, INDEX_URL_NAME, LOGIN_URL_NAME, \
  UNAUTHORIZED_CODE, \
  CONFLICT_CODE
from store.utils.errors import AUTH_ERROR
from store.views.constants import LOGIN_TEMPLATE, ERROR_TEMPLATE


class LoginView(View):
  def get(self, request):
    return render(request, LOGIN_TEMPLATE)

  def post(self, request):
    if (request.user.is_authenticated):
      return render(request, ERROR_TEMPLATE, status=CONFLICT_CODE)
    user = authenticate(username=request.POST.get(USERNAME_KEY), password=request.POST.get(PASSWORD_KEY))
    if not user:
      return render(request, LOGIN_TEMPLATE, {ERRORS_KEY: {AUTH_KEY: AUTH_ERROR}}, status=UNAUTHORIZED_CODE)
    login(request, user)
    return HttpResponseRedirect(reverse_lazy(INDEX_URL_NAME))


class LogoutView(View):
  def get(self, request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy(LOGIN_URL_NAME))
