from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.shortcuts import reverse
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None):
        if not username:
            raise ValueError("Username required")
        if self.model.objects.filter(username=username):
            raise ValueError("User already exists")
        user = self.model(
            # email=self.normalize_email(email),
            username=self.normalize_email(username),
        )
        user.authenticated = True
        user.anonymous = False
        user.email = self.normalize_email(email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, password):
        user = self.create_user(username, password)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):#models.Model
    id = models.IntegerField(unique=True)
    username = models.CharField(primary_key=True, max_length=20)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    anonymous = models.BooleanField(default=False)
    authenticated = models.BooleanField(default=False)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    task_count = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    def get_username(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.id is None:
            self.id = User.objects.all().count()
        # self.authenticated = True
        super(User, self).save(*args, **kwargs)

    def __unicode__(self):
        return "Custom user model"

    def get_absolute(self):
        return reverse('prof-url' + self.pk, kwargs={'pk': self.pk})

    def __str__(self):

        return self.username

    def authenticate(self):
        self.authenticated = True

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_anonymous(self):
        return self.anonymous

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return True

    @property
    def is_admin(self):
        return self.admin

