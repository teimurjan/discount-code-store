from django.contrib.auth.models import User
from django.test import TestCase

from store.tests.constants import COMMON_PASSWORD
from store.utils.constants import FOUND_CODE


class TestCaseWithLogin(TestCase):
  def login(self, user):
    logged_in = self.client.login(username=user.username, password=COMMON_PASSWORD)
    self.assertEquals(logged_in, True)


class TestCaseWithSetUpUsers(TestCase):
  fixtures = ['users.json']

  def setUp(self):
    self.staff_user = User.objects.filter(is_staff=True)[0]
    self.simple_user = User.objects.filter(is_staff=False)[0]


class TestWithCheckingRedirect(TestCase):
  def check_for_redirect(self, method, url, redirect_url, data=None):
    response = getattr(self.client, method)(url, data)
    self.assertEquals(response.status_code, FOUND_CODE)
    self.assertEquals(response.url, redirect_url)
    return response
