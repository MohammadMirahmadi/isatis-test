from rest_framework import serializers
from .models import Category, Book, Reservation
from user.models import AllUser

# serializer برای فیلدهای دسته بندی
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['cid', 'name', 'description']

# serializer برای فیلدهای کتاب
class BookSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='cid')

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'category', 'availability_status', 'bid']

# serializer برای رزرو کردن کتاب
class ReservationSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(queryset=Book.objects.all(), slug_field='bid')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'book', 'reservation_date', 'return_date', 'rid']
        read_only_fields = ['reservation_date', 'rid', 'user']

    def validate(self, attrs):
        book = attrs.get('book')
        if not book.availability_status:
            raise serializers.ValidationError("This book is not available for reservation.")
        return attrs

# serializer مشخصات کاربر رزرو کننده (برای رابطه ها)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllUser
        fields = ['name', 'phone_number', 'national_code']

# serializer مشخصات رزرو کتاب (برای رابطه ها)
class GetReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Reservation
        fields = ['rid', 'user', 'reservation_date', 'return_date']

# serializer دیدن مشخصات کتاب
class BookDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    reservation = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['bid', 'title', 'author', 'published_date', 'availability_status', 'category', 'reservation']

    def get_reservation(self, obj):
        reservation = obj.reservation_set.filter(return_date__isnull=True).first()
        if reservation:
            return ReservationSerializer(reservation).data
        return None

# serializer برای دیدن کتاب هایی که هر کاربر رزرو کرده است و بازگرداندن کتاب  
class UserReservationSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()
    book_details = serializers.SerializerMethodField()
    reservation_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    return_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = Reservation
        fields = ['rid', 'book', 'book_details', 'reservation_date', 'return_date']

    def get_book_details(self, obj):
        return {
            "bid": obj.book.bid,
            "title": obj.book.title,
            "author": obj.book.author,
            "published_date": obj.book.published_date,
        }

# serializer برای دیدن کل کتاب ها
class SimpleBookSerializer(serializers.ModelSerializer):
    is_reserved = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['bid', 'title', 'author', 'published_date', 'is_reserved']

    def get_is_reserved(self, obj):
        return obj.reservation_set.filter(return_date__isnull=True).exists()

# serializer برای رابطه بین کتاب و دسته بندی 
class BookWithReservationSerializer(serializers.ModelSerializer):
    reservation = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['bid', 'title', 'author', 'published_date', 'availability_status', 'reservation']

    def get_reservation(self, obj):
        reservation = obj.reservation_set.filter(return_date__isnull=True).first()
        if reservation:
            return ReservationSerializer(reservation).data
        return None

# serializer کتاب های هر دسته بندی
class CategoryWithBooksSerializer(serializers.ModelSerializer):
    books = BookWithReservationSerializer(many=True, source='book_set')

    class Meta:
        model = Category
        fields = ['cid', 'name', 'description', 'books']