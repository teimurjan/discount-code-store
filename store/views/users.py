from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from store.utils.constants import USERNAME_KEY, USERS_KEY
from store.views.constants import USERS_TEMPLATE, FIND_USER_TEMPLATE


class UsersView(View):
  @method_decorator(staff_member_required(redirect_field_name=None))
  def get(self, request):
    username_query = request.GET.get(USERNAME_KEY)
    if username_query is None:
      username_query = ''
    users_found = User.objects.filter(username__contains=username_query, is_staff=False)
    return render(request, USERS_TEMPLATE, {USERS_KEY: users_found})


class FindUserView(View):
  @method_decorator(staff_member_required(redirect_field_name=None))
  def get(self, request):
    return render(request, FIND_USER_TEMPLATE)