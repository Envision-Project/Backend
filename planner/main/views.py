from django.shortcuts import render, redirect
from rest_framework import viewsets, status, filters
from .serializers import TasksSerializer, TaskListSerializer, UserSerializer, LoginSerializer, RegisterSerializer
from .models import Tasks, Task_List, User
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

class LoginViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response({
            "user": serializer.data,
            "refresh": res["refresh"],
            "token": res["access"]
        }, status=status.HTTP_201_CREATED)


class RefreshViewSet(viewsets.ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated']
    ordering = ['-updated']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]

        obj = User.objects.get(lookup_field_value)
        self.check_object_permissions(self.request, obj)

        return obj

# Create your views here.
class TasksViewSet(viewsets.ModelViewSet):
    serializer_class = TasksSerializer
    queryset = Tasks.objects.all()

class TaskListViewSet(viewsets.ModelViewSet):
    serializer_class = TaskListSerializer
    queryset = Task_List.objects.all()

def addTask(request):
    serializer = TasksSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response("Success")
    else:
        return Response(serializer.errors)

def addTaskList(request):
    serializer = TaskListSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response("Success")
    else:
        return Response(serializer.errors)

def updateTask(request, task_id, field, value):
    task_id = int(task_id)

    try:
        task_sel = Tasks.objects.get(task_id = task_id)
    except Tasks.DoesNotExist:
        return redirect('index')
    
    task_sel.field = value
    task_sel.save()

def updateTaskList(request, task_list_id, field, value):
    task_list_id = int(task_list_id)

    try:
        taskList_sel = Task_List.objects.get(task_list_id = task_list_id)
    except Task_List.DoesNotExist:
        return redirect('index')
    
    taskList_sel.field = value
    taskList_sel.save()

def deleteTask(request, task_id):
    task_id = int(task_id)
    try:
        task_sel = Tasks.objects.get(task_id = task_id)
    except Tasks.DoesNotExist:
        return redirect('index')
    task_sel.delete()
    return redirect('index')

def deleteTaskList(request, task_list_id):
    task_list_id = int(task_list_id)
    try:
        task_list_sel = Task_List.objects.get(task_list_id = task_list_id)
    except Task_List.DoesNotExist:
        return redirect('index')
    task_list_sel.delete()
    return redirect('index')

