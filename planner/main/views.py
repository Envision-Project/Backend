from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TasksSerializer, TaskListSerializer
from .models import Tasks, Task_List
from django.http import HttpResponse, JsonResponse

# Create your views here.
class TasksViewSet(viewsets.ModelViewSet):
    serializer_class = TasksSerializer
    queryset = Tasks.objects.all()

class TaskListViewSet(viewsets.ModelViewSet):
    serializer_class = TaskListSerializer
    queryset = Task_List.objects.all()
