from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ProfileSerializer
from .models import Profile
from rest_framework import mixins
from .permissions import IsAnonymous
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ProfileSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response



@api_view(['POST'])
@csrf_exempt
def signup_view(request):
    Profile = get_user_model()
    data = request.data
    serializer = ProfileSerializer(data=data)
    try:
        serializer.is_valid(raise_exception=True)
    except Exception:
        return Response('Use another username or email', status=status.HTTP_400_BAD_REQUEST)

    user = Profile.objects.create_user(email=data['email'], password=data['password'],
                                    username=data['username'], city=data['city'])

    return Response(ProfileSerializer(user).data, status=status.HTTP_201_CREATED)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes_by_action = {
        'create': [IsAnonymous],
        'retrieve': [permissions.IsAdminUser],
        'update': [permissions.IsAuthenticated],
        'partial_update': [permissions.IsAdminUser],
        'destroy': [permissions.IsAdminUser],
        'list': [permissions.IsAdminUser],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
