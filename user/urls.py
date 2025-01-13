from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('user-register/', UserRegistrationView.as_view(), name='user-registration'), # ثبت نام کاربر عادی
    path('create-superuser/', CreateSuperUserView.as_view(), name='create_superuser'), # ثب نام سوپریوزر
    path('login/', LoginView.as_view(), name='login'), # login
    path('logout/', LogoutView.as_view(), name='logout'), # logout
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'), # دریافت accestoken با refreshtoken
    path('edit-profile/', AllUserEditView.as_view(), name='edit_profile'), # ویرایش مشخصات کاربران
    path('change-password/', ChangePasswordView.as_view(), name='change-password'), # عوض کردن رمز توسط کاربر
    path('user/toggle-status/<str:user_uid>/', ToggleUserStatusView.as_view(), name='toggle-user-status'), # فعال و غیرفعال کردن کاربران
    path('user-detail/<str:uid>/', UserDetailView.as_view(), name='user-detail'), # دیدن مشخصات کاربران وکتاب های رزرو کرده 
    path('users-list/', AllUserListView.as_view(), name='all-user-list'), # لیست تمام کاربران
]
    

