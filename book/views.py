from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from django.db import transaction
from .models import Category, Book, Reservation
from .serializers import CategorySerializer, BookSerializer, ReservationSerializer, BookDetailSerializer, UserReservationSerializer, SimpleBookSerializer, CategoryWithBooksSerializer
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError
from .throttling import IsUserRateThrottle

# view برای ساخت دسته بندی
class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            try:
                with transaction.atomic():
                    serializer.save()
            except Exception as e:
                raise Response({"error": f"Error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            raise PermissionError("Only superusers can create categories.")

# view برای اضافه کردن کتاب
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            response = super().create(request, *args, **kwargs)
            return response

# view برای رزرو کردن کتاب     
class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [IsUserRateThrottle] # محدود کردن تعداد درخواست برای کاربر عادی

    def perform_create(self, serializer):
        with transaction.atomic():
            book = serializer.validated_data['book']

            book.availability_status = False
            book.save()

            serializer.save(user=self.request.user)

# view برای دیدن مشخصات کتاب
class BookDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    lookup_field = 'bid'
    throttle_classes = [IsUserRateThrottle] # محدود کردن تعداد درخواست برای کاربر عادی

# view برای دیدن کتاب هایی که هر کاربر رزرو کرده است
class UserReservationListView(generics.ListAPIView):
    serializer_class = UserReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

# view بازگرداندن کتاب
class ReturnBookView(generics.UpdateAPIView):
    serializer_class = UserReservationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'rid'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user, return_date__isnull=True)

    def perform_update(self, serializer):
        with transaction.atomic():
            reservation = self.get_object()
            reservation.return_date = now()
            reservation.save()

            reservation.book.availability_status = True
            reservation.book.save()

            serializer.instance = reservation

# view برای دیدن کل کتاب ها همراه با سرچ
class BookListView(generics.ListAPIView):
    serializer_class = SimpleBookSerializer
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'author', 'category__name']
    filterset_fields = ['category__name'] 

# view برای دیدن همه دسته بندی ها
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# view برای دیدن مشخصات و همه کتاب های زیر مجموعه هر دسته بندی
class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithBooksSerializer
    lookup_field = 'cid'
    permission_classes = [IsAuthenticated]

# view ویرایش دسته بندی
class CategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CategorySerializer
    lookup_field = 'cid'

# view ویرایش مشخصات کتاب
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BookSerializer
    lookup_field = 'bid'

# view حذف کردن کتاب
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BookSerializer
    lookup_field = 'bid'

    def perform_destroy(self, instance):
        if instance.availability_status:
            instance.delete()
        else:
            raise ValidationError("Only books with availability status 'True' can be deleted.")