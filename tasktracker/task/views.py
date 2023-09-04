from django.shortcuts import render
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from rest_framework import filters
from .permissions import IsAdminOrIsOwner
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['owner__username']
    search_fields = ['category', 'priority', 'status']
    permission_classes_by_action = {
        'create': [permissions.IsAuthenticated],
        'retrieve': [IsAdminOrIsOwner],
        'update': [IsAdminOrIsOwner],
        'partial_update': [IsAdminOrIsOwner],
        'destroy': [IsAdminOrIsOwner],
        'list': [permissions.IsAdminUser],
    }

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def my_tasks(self, request):
        queryset = Task.objects.filter(owner=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
    

