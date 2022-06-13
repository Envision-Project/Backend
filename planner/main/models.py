from tkinter import CASCADE
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a `User` with an email, phone number, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must have an email.')
        if username is None:
            raise TypeError('Superusers must have an username.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(primary_key=True, db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True,  null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"
        
class Task_List(models.Model):
    task_list_id = models.AutoField(primary_key=True)
    task_list_name = models.CharField(max_length=120)
    color = models.CharField(max_length=120)

    def _str_(self):
        return self.task_list_name

class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.IntegerField(null=True,  validators=[MaxValueValidator(5), MinValueValidator(1)])
    task_list_id = models.ForeignKey("Task_List", on_delete=models.CASCADE)
    
    def _str_(self):
        return self.title

class User_TaskList(models.Model):
    username = models.ForeignKey("User", on_delete=models.CASCADE)
    task_list_id = models.ForeignKey("Task_List", on_delete=models.CASCADE)

