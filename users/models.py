from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres import fields as postgres
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from polymorphic.models import PolymorphicModel, PolymorphicManager


class UserManager(PolymorphicManager, BaseUserManager):
    
    def create_user(self, login, display_name, password, **kwargs):
        user = User(login=login, display_name=display_name, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, login, display_name, password):
        return self.create_user(login, display_name, password)
    


class User(PolymorphicModel, AbstractBaseUser):

    login = models.SlugField(max_length=254, unique=True)
    display_name = models.CharField(max_length=30)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ('display_name',)

    objects = UserManager()
    