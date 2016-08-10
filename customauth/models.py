from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, activation_code, password=None):
        """
        Creates and saves a user with the give email and password
        :param email:
        :param password:
        :return:
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(email=self.normalize_email(email), username=username, activation_code=activation_code)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, activation_code, password):
        activation_code = 'asdfasdf'
        user = self.create_user(email, username, activation_code,  password=password)
        user.is_admin = True

        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    username = models.CharField(
        verbose_name='username',
        max_length=255,
        unique=True
    )

    activation_code = models.CharField(
        verbose_name='activation code',
        max_length=32,
        unique=True
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'activation_code']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin