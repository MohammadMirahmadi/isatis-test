from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .models import AllUser
from .serializers import CreateUserSerializer, SuperUserCreationSerializer, AllUserUpdateSerializer, ChangePasswordSerializer, AllUserSerializer, AllUserListSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from rest_framework.mixins import UpdateModelMixin
from rest_framework.filters import SearchFilter

# view ثبت نام کاربر عادی
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": {
                    "name": user.name,
                    "phone_number": user.phone_number,
                    "national_code": user.national_code,
                    "is_user": user.is_user,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# view ثب نام سوپریوزر
class CreateSuperUserView(generics.CreateAPIView):
    serializer_class = SuperUserCreationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                user = serializer.save()
                return user
        except Exception as e:
            raise ValueError(f"Failed to create superuser: {str(e)}")

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.get_serializer().instance

        return Response({
            "message": "Superuser created successfully",
            "user": {
                "username": user.username,
                "name": user.name,
                "national_code": user.national_code,
                "phone_number": user.phone_number,
            }
        }, status=status.HTTP_201_CREATED)

# view برای login
class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        if not phone_number or not password:
            return Response({"detail": "Phone number and password are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            role = "user" if user.is_user else "admin" if user.is_superuser else "unknown"

            return Response({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "role": role,
                "user": {
                    "name": user.name,
                    "phone_number": user.phone_number,
                    "national_code": user.national_code,
                }
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid phone number or password."},
                        status=status.HTTP_401_UNAUTHORIZED)

# view برای logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# view ویرایش مشخصات کاربران
class AllUserEditView(generics.RetrieveUpdateAPIView):
    serializer_class = AllUserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    return Response({
                        "message": "Profile updated successfully",
                        "user": {
                            "name": user.name,
                            "phone_number": user.phone_number,
                            "national_code": user.national_code,
                        }
                    }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# view عوض کردن رمز توسط کاربر
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# view فعال و غیرفعال کردن کاربران
class ToggleUserStatusView(generics.GenericAPIView, UpdateModelMixin):
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = AllUser.objects.all()
    serializer_class = None

    def get_object(self):
        user_uid = self.kwargs.get('user_uid')
        try:
            return AllUser.objects.get(uid=user_uid)
        except AllUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()

        if request.user.is_superuser:
            if user.is_user:
                try:
                    with transaction.atomic():
                        user.is_active = not user.is_active
                        user.save()

                    return Response({
                        "message": f"User's status changed to {'active' if user.is_active else 'inactive'}"
                    }, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"error": "User's status cannot be changed. This user is not active."}, status=status.HTTP_403_FORBIDDEN)
        
        return Response({"error": "You do not have permission to modify this field."}, status=status.HTTP_403_FORBIDDEN)

# view دیدن مشخصات کاربران وکتاب های رزرو کرده
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, uid, format=None):
        try:
            user = AllUser.objects.get(uid=uid)
        except AllUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)
        
        serializer = AllUserSerializer(user)
        return Response(serializer.data)
# view لیست تمام کاربران
class AllUserListView(generics.ListAPIView):
    queryset = AllUser.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = AllUserListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'phone_number']