from rest_framework import serializers
from .models import Tasks

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('task_id', 'title', 'description', 'due_date', 'priority', 'task_list_id')