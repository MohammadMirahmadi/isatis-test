from django.contrib import admin
from .models import AllUser

# تعریف مدل مشخصات کاربران برای پنل ادمین
@admin.register(AllUser)
class AllUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'national_code', 'is_user', 'is_superuser')
    search_fields = ('name', 'phone_number', 'national_code')
    list_filter = ('is_user',)
    ordering = ('name',)
