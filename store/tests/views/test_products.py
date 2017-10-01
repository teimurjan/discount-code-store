from django.shortcuts import resolve_url
from django.urls import reverse

from store.models import Product, Code
from store.tests.constants import GET, STAFF_REQUIRED_REDIRECT_URL, POST
from store.tests.views.base import TestWithCheckingRedirect, TestCaseWithLogin, TestCaseWithSetUpUsers
from store.utils.constants import PRODUCTS_URL_NAME, OK_STATUS_CODE, PRODUCTS_KEY, INDEX_URL_NAME, PRODUCT_KEY, \
  BAD_REQUEST_CODE, NOT_FOUND_CODE


class ProductViewTest(TestCaseWithLogin, TestCaseWithSetUpUsers, TestWithCheckingRedirect):
  fixtures = TestCaseWithSetUpUsers.fixtures + ['products_view_test.json']

  def test_should_get_successfully(self):
    self.login(self.staff_user)
    response = self.client.get(reverse(PRODUCTS_URL_NAME))
    self.assertEquals(response.status_code, OK_STATUS_CODE)
    self.assertEquals(list(response.context[PRODUCTS_KEY]), list(Product.objects.all()))

  def test_should_get_requires_staff(self):
    self.login(self.simple_user)
    self.check_for_redirect(GET, reverse(PRODUCTS_URL_NAME), resolve_url(STAFF_REQUIRED_REDIRECT_URL))

  def test_should_post_successfully(self):
    self.login(self.staff_user)
    product = Product.objects.all()[0]
    self.check_for_redirect(POST, '{0}?user={1}'.format(reverse(PRODUCTS_URL_NAME), self.simple_user.pk),
                            reverse(INDEX_URL_NAME), data={PRODUCT_KEY: product.pk})
    self.assertTrue(Code.objects.filter(assigner_id=self.staff_user.pk,
                                        assignee_id=self.simple_user.pk,
                                        product=product.pk).exists())

  def test_should_post_staff_user_id_as_assignee(self):
    self.login(self.staff_user)
    product = Product.objects.all()[0]
    response = self.client.post('{0}?user={1}'.format(reverse(PRODUCTS_URL_NAME), self.staff_user.pk),
                                {PRODUCT_KEY: product.pk})
    self.assertEquals(response.status_code, BAD_REQUEST_CODE)

  def test_should_post_no_data(self):
    self.login(self.staff_user)
    response = self.client.post(reverse(PRODUCTS_URL_NAME))
    self.assertEquals(response.status_code, BAD_REQUEST_CODE)

  def test_should_post_invalid_user(self):
    self.login(self.staff_user)
    product = Product.objects.all()[0]
    invalid_user_id = 999
    response = self.client.post('{0}?user={1}'.format(reverse(PRODUCTS_URL_NAME), invalid_user_id),
                                {PRODUCT_KEY: product.pk})
    self.assertEquals(response.status_code, NOT_FOUND_CODE)

  def test_should_post_invalid_product(self):
    self.login(self.staff_user)
    invalid_product_id = 999
    response = self.client.post('{0}?user={1}'.format(reverse(PRODUCTS_URL_NAME), self.simple_user.pk),
                                {PRODUCT_KEY: invalid_product_id})
    self.assertEquals(response.status_code, NOT_FOUND_CODE)

  def test_should_post_requires_staff(self):
    self.login(self.simple_user)
    product = Product.objects.all()[0]
    self.check_for_redirect(POST, '{0}?user={1}'.format(reverse(PRODUCTS_URL_NAME), self.staff_user.pk),
                            resolve_url(STAFF_REQUIRED_REDIRECT_URL), data={PRODUCT_KEY: product.pk})
