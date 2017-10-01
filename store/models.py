from django.contrib.auth.models import User
from django.db import models

from store.utils.constants import DISCOUNT_CODE_FORMAT_REGEX


class Product(models.Model):
  name = models.CharField(blank=False, null=False, max_length=255)
  price = models.IntegerField(null=False)


class Code(models.Model):
  value = models.CharField(blank=False, null=False, max_length=255, unique=True)
  assignee = models.ForeignKey(User, related_name='codes')
  assigner = models.ForeignKey(User, related_name='assigned_codes')
  product = models.ForeignKey(Product)

  @staticmethod
  def generate_unique_code():
    import rstr
    code = rstr.xeger(DISCOUNT_CODE_FORMAT_REGEX)
    if Code.objects.filter(value=code).exists():
      return Code.generate_unique_code()
    return code

  def save(self, *args, **kwargs):
    if not self.value:
      self.value = Code.generate_unique_code()
    return super(Code, self).save(*args, **kwargs)
