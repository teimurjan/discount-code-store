from django.urls import reverse

from store.tests.constants import COMMON_PASSWORD, LOGGED_IN_USER_SESSION_KEY, GET, POST
from store.tests.views.base import TestCaseWithLogin, TestCaseWithSetUpUsers, TestWithCheckingRedirect
from store.utils.constants import LOGIN_URL_NAME, OK_STATUS_CODE, PASSWORD_KEY, FOUND_CODE, USERNAME_KEY, \
  INDEX_URL_NAME, UNAUTHORIZED_CODE, ERRORS_KEY, AUTH_KEY, CONFLICT_CODE, LOGOUT_URL_NAME
from store.utils.errors import AUTH_ERROR
from store.views.constants import LOGIN_TEMPLATE, ERROR_TEMPLATE


class LoginViewTest(TestCaseWithLogin, TestCaseWithSetUpUsers, TestWithCheckingRedirect):
  def test_should_get_successfully(self):
    response = self.client.get(reverse(LOGIN_URL_NAME))
    self.assertEquals(response.status_code, OK_STATUS_CODE)
    self.assertEquals(response.templates[0].name, LOGIN_TEMPLATE)

  def test_should_post_successfully(self):
    auth_data = {USERNAME_KEY: self.simple_user.username, PASSWORD_KEY: COMMON_PASSWORD}
    self.check_for_redirect(POST, reverse(LOGIN_URL_NAME), reverse(INDEX_URL_NAME), auth_data)
    self.assertIn(LOGGED_IN_USER_SESSION_KEY, self.client.session)

  def test_should_post_invalid_auth_data(self):
    auth_data = {USERNAME_KEY: 'invalid', PASSWORD_KEY: 'invalid'}
    response = self.client.post(reverse(LOGIN_URL_NAME), auth_data)
    self.assertEquals(response.status_code, UNAUTHORIZED_CODE)
    self.assertEquals(response.context[ERRORS_KEY][AUTH_KEY], AUTH_ERROR)

  def test_should_post_when_authenticated(self):
    self.login(self.simple_user)
    auth_data = {USERNAME_KEY: self.simple_user.username, PASSWORD_KEY: COMMON_PASSWORD}
    response = self.client.post(reverse(LOGIN_URL_NAME), auth_data)
    self.assertEquals(response.status_code, CONFLICT_CODE)
    self.assertEquals(response.templates[0].name, ERROR_TEMPLATE)


class LogoutViewTest(TestCaseWithSetUpUsers, TestCaseWithLogin, TestWithCheckingRedirect):
  def test_should_logout_successfully(self):
    self.login(self.simple_user)
    self.check_for_redirect(GET, reverse(LOGOUT_URL_NAME), reverse(LOGIN_URL_NAME))
    self.assertNotIn(LOGGED_IN_USER_SESSION_KEY, self.client.session)