from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres import fields as postgres
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from polymorphic.models import PolymorphicModel, PolymorphicManager


class UserManager(PolymorphicManager, BaseUserManager):
    
    def create_user(self, login, password, **kwargs):
        user = User(login=login, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, login, password):
        return self.create_user(login, password)
    


class User(PolymorphicModel, AbstractBaseUser):

    login = models.SlugField(max_length=254, unique=True)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ()

    objects = UserManager()
    