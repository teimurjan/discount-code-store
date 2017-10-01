from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.urls import reverse

from store.tests.constants import GET, STAFF_REQUIRED_REDIRECT_URL
from store.tests.views.base import TestCaseWithSetUpUsers, TestCaseWithLogin, TestWithCheckingRedirect
from store.utils.constants import USERS_URL_NAME, OK_STATUS_CODE, USERS_KEY, FIND_USERS_URL_NAME, USERNAME_KEY


class UsersViewTest(TestCaseWithSetUpUsers, TestCaseWithLogin, TestWithCheckingRedirect):
  def test_should_get_successfully(self):
    self.login(self.staff_user)
    response = self.client.get(reverse(USERS_URL_NAME))
    self.assertEquals(response.status_code, OK_STATUS_CODE)
    expected_users = User.objects.filter(is_staff=False)
    self.assertEquals(list(response.context[USERS_KEY]), list(expected_users))

  def test_should_get_with_filter(self):
    self.login(self.staff_user)
    username_chunk = self.simple_user.username[:3]
    response = self.client.get(reverse(USERS_URL_NAME), {USERNAME_KEY: username_chunk})
    self.assertEquals(response.status_code, OK_STATUS_CODE)
    expected_users = User.objects.filter(username__contains=username_chunk, is_staff=False)
    self.assertEquals(list(response.context[USERS_KEY]), list(expected_users))

  def test_should_require_staff(self):
    self.login(self.simple_user)
    self.check_for_redirect(GET, reverse(USERS_URL_NAME), resolve_url(STAFF_REQUIRED_REDIRECT_URL))


class FindUserViewTest(TestCaseWithSetUpUsers, TestCaseWithLogin, TestWithCheckingRedirect):
  def test_should_get_successfully(self):
    self.login(self.staff_user)
    response = self.client.get(reverse(FIND_USERS_URL_NAME))
    self.assertEquals(response.status_code, OK_STATUS_CODE)

  def test_should_require_staff(self):
    self.login(self.simple_user)
    self.check_for_redirect(GET, reverse(FIND_USERS_URL_NAME), resolve_url(STAFF_REQUIRED_REDIRECT_URL))
