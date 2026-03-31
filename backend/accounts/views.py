from rest_framework import viewsets, generics, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, UserDetailSerializer
from .permissions import IsSystemAdministrator

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSystemAdministrator] 

    def get_queryset(self):
        user = self.request.user
        if user.hospital:
            return User.objects.filter(hospital=user.hospital)
        return User.objects.all()

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
