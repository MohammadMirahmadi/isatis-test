from django.urls import path
from .views import *

urlpatterns = [
    path('create-category/', CategoryCreateView.as_view(), name='create-category'), # ساخت دسته بندی
    path('create-book/', BookCreateView.as_view(), name='create-book'), # اضافه کردن کتاب
    path('reserve-book/', ReservationCreateView.as_view(), name='reserve-book'), # رزرو کردن کتاب
    path('book-detail/<str:bid>/', BookDetailView.as_view(), name='book-detail'), #  دیدن مشخصات کتاب
    path('books-list/', BookListView.as_view(), name='book-list'), # دیدن لیست کلیه کتاب ها
    path('user/reservations/', UserReservationListView.as_view(), name='user-reservations'), # دیدن کتاب هایی که هر کاربر رزرو کرده است
    path('user/reservations/<str:rid>/return/', ReturnBookView.as_view(), name='return-book'), # بازگرداندن کتاب
    path('categories-list/', CategoryListView.as_view(), name='category-list'), # برای دیدن همه دسته بندی ها
    path('category-detail/<str:cid>/', CategoryDetailView.as_view(), name='category-detail'), # برای دیدن مشخصات و همه کتاب های زیر مجموعه هر دسته بندی
    path('edit-category/<str:cid>/', CategoryUpdateView.as_view(), name='category-update'), # ویرایش دسته بندی
    path('edit-books/<str:bid>/', BookUpdateView.as_view(), name='book-update'), # ویرایش مشخصات کتاب
    path('books/<str:bid>/delete/', BookDeleteView.as_view(), name='book-delete'), # حذف کردن کتاب
]
