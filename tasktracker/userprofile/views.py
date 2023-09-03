from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ProfileSerializer
from .models import Profile
from rest_framework import mixins
from .permissions import IsAnonymous, IsAdminOrIsSelf
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import filters
from django.shortcuts import get_object_or_404

@api_view(['POST'])
@permission_classes([IsAnonymous])
@csrf_exempt
def signup_view(request):
    Profile = get_user_model()
    data = request.data
    serializer = ProfileSerializer(data=data)
    try:
        serializer.is_valid(raise_exception=True)
    except Exception:
        return Response({'detail':'Use another username or email'}, status=status.HTTP_400_BAD_REQUEST)

    user = Profile.objects.create_user(email=data['email'], password=data['password'],
                                    username=data['username'], city=data['city'])

    return Response(ProfileSerializer(user).data, status=status.HTTP_201_CREATED)


class ProfileViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['username', 'email']
    search_fields = ['username', 'email', 'city']
    permission_classes_by_action = {
        'retrieve': [IsAdminOrIsSelf],
        'update': [IsAdminOrIsSelf],
        'partial_update': [IsAdminOrIsSelf],
        'destroy': [IsAdminOrIsSelf],
        'list': [permissions.IsAdminUser],
    }

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def my_settings(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['PATCH', 'PUT'], permission_classes=[permissions.IsAuthenticated])
    def edit_settings(self, request):
        partial = request.method == 'PATCH'
        serializer = self.get_serializer(request.user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    
    @action(detail=False, methods=['DELETE'], permission_classes=[permissions.IsAuthenticated])
    def delete_account(self, request):
        obj = request.user
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
