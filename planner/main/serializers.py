from rest_framework import serializers
from .models import Task_List, Tasks

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_List
        fields = '__all__'