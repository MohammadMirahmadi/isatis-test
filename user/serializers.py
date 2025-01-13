from django.db import transaction
from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import AllUser
import re
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from book.models import Book, Reservation

# serializer ثبت نام کاربر عادی
class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = AllUser
        fields = ['name', 'phone_number', 'national_code', 'password']
        extra_kwargs = {
            'is_user': {'default': True},
        }

    def validate_phone_number(self, value):

        if len(value) != 11:
            raise serializers.ValidationError("Phone number must be 11 digits long.")
        if AllUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def validate_national_code(self, value):

        if len(value) != 10:
            raise serializers.ValidationError("National code must be 10 digits long.")
        if AllUser.objects.filter(national_code=value).exists():
            raise serializers.ValidationError("This national code is already registered.")
        return value

    def validate_password(self, value):

        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r'[a-zA-Z]', value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        return value

    def create(self, validated_data):

        with transaction.atomic():
            user = AllUser.objects.create_user(
                username=validated_data['name'] + validated_data['phone_number'],
                name=validated_data['name'],
                phone_number=validated_data['phone_number'],
                national_code=validated_data['national_code'],
                password=validated_data['password'],
                is_user=True
            )
            return user

User = get_user_model()

# serializer ثب نام سوپریوزر
class SuperUserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'name', 'password', 'national_code', 'phone_number']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value
    
    def validate_phone_number(self, value):

        if len(value) != 11:
            raise serializers.ValidationError("Phone number must be 11 digits long.")
        if AllUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def validate_national_code(self, value):
        if User.objects.filter(national_code=value).exists():
            raise serializers.ValidationError("This national code is already in use.")
        return value
    
    def validate_password(self, value):

        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r'[a-zA-Z]', value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        return value

    def create(self, validated_data):

        return User.objects.create_superuser(
            username=validated_data['username'],
            name=validated_data['name'],
            password=validated_data['password'],
            national_code=validated_data['national_code'],
            phone_number=validated_data['phone_number'],
        )

# serializer ویرایش مشخصات کاربران
class AllUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllUser
        fields = ['name', 'phone_number', 'national_code']

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) != 11:
            raise serializers.ValidationError("Phone number must be exactly 11 digits.")
        return value

    def validate_national_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("National code must contain only digits.")
        if len(value) != 13:
            raise serializers.ValidationError("National code must be exactly 13 digits.")
        return value
    
# serializer عوض کردن رمز توسط کاربر
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate_password(self, value):

        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r'[a-zA-Z]', value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("The new password and confirmation password do not match.")
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.password = make_password(new_password)
        user.save(update_fields=['password'])
        return user

# serializer رابطه بین کتاب و رزرو کتاب
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['rid', 'book', 'reservation_date', 'return_date']

# serializer رابطه بین کاربر و کتاب
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['bid', 'title', 'author', 'published_date', 'availability_status']

# serializer دیدن مشخصات کاربران وکتاب های رزرو کرده
class AllUserSerializer(serializers.ModelSerializer):
    reserved_books = serializers.SerializerMethodField()

    class Meta:
        model = AllUser
        fields = ['uid', 'username', 'name', 'phone_number', 'national_code', 'is_user', 'reserved_books']

    def get_reserved_books(self, obj):
        reservations = Reservation.objects.filter(user=obj)
        books = [reservation.book for reservation in reservations]
        return BookSerializer(books, many=True).data

# serializer لیست تمام کاربران
class AllUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllUser
        fields = ['uid', 'name', 'phone_number', 'national_code']
