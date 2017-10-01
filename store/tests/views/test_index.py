from django.contrib.auth.models import User
from django.urls import reverse

from store.tests.constants import GET
from store.tests.views.base import TestCaseWithLogin, TestCaseWithSetUpUsers, TestWithCheckingRedirect
from store.utils.constants import OK_STATUS_CODE, INDEX_URL_NAME, DISCOUNT_CODES_KEY, LOGIN_URL_NAME
from store.views.constants import USER_INDEX_TEMPLATE, STAFF_INDEX_TEMPLATE


class IndexViewTest(TestCaseWithLogin, TestCaseWithSetUpUsers, TestWithCheckingRedirect):
  fixtures = TestCaseWithSetUpUsers.fixtures + ['index_view_test.json']

  def setUp(self):
    self.staff_user = User.objects.filter(is_staff=True)[0]
    self.simple_user = User.objects.filter(is_staff=False)[0]

  def test_should_get_index_for_simple_user(self):
    self.login(self.simple_user)
    response = self.client.get(reverse(INDEX_URL_NAME))
    self.assertEquals(response.status_code, OK_STATUS_CODE)
    self.assertEquals(response.templates[0].name, USER_INDEX_TEMPLATE)
    self.assertEquals(list(response.context[DISCOUNT_CODES_KEY]), list(self.simple_user.codes.all()))

  def test_should_get_index_for_staff_user(self):
    self.login(self.staff_user)
    response = self.client.get(reverse(INDEX_URL_NAME))
    self.assertEquals(response.status_code, OK_STATUS_CODE)
    self.assertEquals(response.templates[0].name, STAFF_INDEX_TEMPLATE)
    self.assertEquals(list(response.context[DISCOUNT_CODES_KEY]), list(self.staff_user.assigned_codes.all()))

  def test_should_require_login(self):
    self.check_for_redirect(GET, reverse(INDEX_URL_NAME), reverse(LOGIN_URL_NAME))
