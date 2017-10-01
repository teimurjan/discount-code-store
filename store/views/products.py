from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

from store.models import Product, Code
from store.utils.constants import USER_KEY, BAD_REQUEST_CODE, PRODUCTS_KEY, PRODUCT_KEY, INDEX_URL_NAME
from store.views.constants import PRODUCTS_TEMPLATE, ERROR_TEMPLATE


class ProductsView(View):
  @method_decorator(staff_member_required(redirect_field_name=None))
  def get(self, request):
    return render(request, PRODUCTS_TEMPLATE, {PRODUCTS_KEY: Product.objects.all()})

  @method_decorator(staff_member_required(redirect_field_name=None))
  def post(self, request):
    user_pk = request.GET.get(USER_KEY)
    product_pk = request.POST.get(PRODUCT_KEY)
    if not user_pk or not product_pk:
      return render(request, ERROR_TEMPLATE, status=BAD_REQUEST_CODE)
    product = get_object_or_404(Product, pk=product_pk)
    assignee = get_object_or_404(User, pk=user_pk)
    if assignee.is_staff:
      return render(request, ERROR_TEMPLATE, status=BAD_REQUEST_CODE)
    assigner = request.user
    Code.objects.create(assignee=assignee, assigner=assigner, product=product)
    return HttpResponseRedirect(reverse_lazy(INDEX_URL_NAME))