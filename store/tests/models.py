from store.models import Code, Product
from store.tests.views.base import TestCaseWithSetUpUsers
import re

from store.utils.constants import DISCOUNT_CODE_FORMAT_REGEX


class CodeTest(TestCaseWithSetUpUsers):
  fixtures = TestCaseWithSetUpUsers.fixtures + ['code_model_test.json']

  def test_should_generate_code_correctly(self):
    product = Product.objects.all()[0]
    for i in range(10):
      code = Code.objects.create(assigner_id=self.staff_user.pk,
                                 assignee_id=self.simple_user.pk,
                                 product_id=product.pk)
      self.assertTrue(re.match(DISCOUNT_CODE_FORMAT_REGEX, code.value))
