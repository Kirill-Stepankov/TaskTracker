from django.urls import include, path
from rest_framework import routers
from . import views
from userprofile.urls import router

router.register(r'tasks', views.TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
