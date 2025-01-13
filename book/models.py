from django.db import models
from shortuuid.django_fields import ShortUUIDField

# مدل دسته بندی کتاب ها
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    cid = ShortUUIDField(unique=True, length=20, alphabet='abcdefghijklmnopqrstuvwxyz1234567890')

    def __str__(self):
        return self.name

# مدل کتاب ها
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    availability_status = models.BooleanField(default=True)
    bid = ShortUUIDField(unique=True, length=20, alphabet='abcdefghijklmnopqrstuvwxyz1234567890')

    def __str__(self):
        return self.title

# مدل رزرو کردن کتاب
class Reservation(models.Model):
    user = models.ForeignKey('user.AllUser', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    rid = ShortUUIDField(unique=True, length=20, alphabet='abcdefghijklmnopqrstuvwxyz1234567890')

    def __str__(self):
        return f"Reservation for {self.user.username} - {self.book.title}"
