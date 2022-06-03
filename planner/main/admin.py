from django.contrib import admin
from .models import Tasks

class TasksAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'title', 'description', 'due_date', 'priority', 'task_list_id')

# Register your models here.

admin.site.register(Tasks, TasksAdmin)