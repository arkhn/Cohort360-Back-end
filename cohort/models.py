from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models

from cohort_back.models import BaseModel


class UserManager(BaseUserManager):
    def create_simple_user(self, username, email, displayname, firstname, lastname):
        user = get_user_model()(
            username=username,
            email=email,
            displayname=displayname,
            firstname=firstname,
            lastname=lastname,
        )
        user.is_active = True
        user.save(using=self.db)
        return user

    def create_super_user(self, *args, **kwargs):
        user = self.create_simple_user(*args, **kwargs)
        user.is_superuser = True
        user.save()


class User(BaseModel, AbstractBaseUser):
    objects = UserManager()

    USERNAME_FIELD = 'username'

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField('email address', max_length=254, unique=True, null=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    displayname = models.CharField(max_length=50, blank=True)
    firstname = models.CharField(max_length=30, blank=True)
    lastname = models.CharField(max_length=30, blank=True)

    def is_admin(self):
        return self.is_superuser
