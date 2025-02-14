
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from apps.commons.ModelUtils import CoreModel


# Create your models here.

class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
      """
      Creates and saves a User with the given email,and password.
      """
      if not email:
        raise ValueError('The given email must be set')

      user = self.model(email=email, **extra_fields)
      user.set_password(password)
      user.save(using=self._db)
      return user

    def create_user(self, email, password, first_name, last_name):
      user = self.model(email=email, first_name=first_name, last_name=last_name)
      user.set_password(password)
      user.is_staff = False
      user.is_active = True
      user.save(using=self._db)
      return user

    def create_superuser(self, email, password, **extra_fields):
      extra_fields.setdefault('is_staff', True)
      extra_fields.setdefault('is_superuser', True)

      return self._create_user(email, password=password, **extra_fields)

    def change_password(self, id, password):
      user = self.model.objects.get(pk=id)
      user.set_password(password)
      return user

class User(AbstractBaseUser, PermissionsMixin, CoreModel):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
      return self.email

    @property
    def token(self):
      refresh = RefreshToken.for_user(self)
      return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
      }

