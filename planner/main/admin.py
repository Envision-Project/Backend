from django.contrib import admin
from .models import Tasks, Task_List

class TasksAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'title', 'description', 'due_date', 'priority', 'task_list_id')

class TaskListAdmin(admin.ModelAdmin):
    list_display = ('task_list_id', 'task_list_name', 'color')

# Register your models here.

admin.site.register(Tasks, TasksAdmin)
admin.site.register(Task_List, TaskListAdmin)