from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

from store.utils.constants import LOGIN_URL_NAME, DISCOUNT_CODES_KEY
from store.views.constants import STAFF_INDEX_TEMPLATE, USER_INDEX_TEMPLATE


class IndexView(View):
  @method_decorator(login_required(login_url=reverse_lazy(LOGIN_URL_NAME), redirect_field_name=None))
  def get(self, request):
    if (request.user.is_staff):
      discount_codes = {DISCOUNT_CODES_KEY: request.user.assigned_codes.all()}
      return render(request, STAFF_INDEX_TEMPLATE, discount_codes)
    discount_codes = {DISCOUNT_CODES_KEY: request.user.codes.all()}
    return render(request, USER_INDEX_TEMPLATE, discount_codes)