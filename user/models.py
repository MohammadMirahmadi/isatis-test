from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
from django.db.models import Max
from django.db.models.signals import pre_save
from django.dispatch import receiver

# مدل تمام کاربران(عادی و سوپریوزر)
class AllUser(AbstractUser):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11, unique=True)
    national_code = models.CharField(max_length=13, unique=True, null=True)
    is_user = models.BooleanField(default=False)
    uid = ShortUUIDField(unique=True, length=20, alphabet='abcdefghijklmnopqrstuvwxyz1234567890')
