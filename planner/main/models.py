from tkinter import CASCADE
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

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
    username = models.ForeignKey("Users", on_delete=models.CASCADE)
    task_list_id = models.ForeignKey("Task_List", on_delete=models.CASCADE)

