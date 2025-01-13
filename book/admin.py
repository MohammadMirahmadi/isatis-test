from django.contrib import admin
from .models import Book, Category, Reservation

# تعریف مدل کتاب برای پنل ادمین
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'category', 'availability_status')
    search_fields = ('title', 'author', 'category__name')
    list_filter = ('availability_status', 'category')
    ordering = ('-published_date',)

admin.site.register(Book, BookAdmin)

# تعریف مدل دسته بندی برای پنل ادمین
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'cid')
    search_fields = ('name', 'cid')
    ordering = ('name',)

admin.site.register(Category, CategoryAdmin)

# تعریف مدل رزرو کتاب برای پنل ادمین
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'reservation_date', 'return_date')
    search_fields = ('user__username', 'book__title')
    list_filter = ('reservation_date', 'return_date')
    ordering = ('-reservation_date',)

admin.site.register(Reservation, ReservationAdmin)