from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, Reservation, Category
from django.contrib.auth import get_user_model

# اسکریپت تست رزرو کردن کتاب توسط کاربر(python manage.py test book)
class ReservationCreateTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Science", description="Books related to science.")

        self.book = Book.objects.create(
            title="Physics 101",
            author="John Doe",
            published_date="2020-01-01",
            category=self.category,
            availability_status=True
        )

        self.user = get_user_model().objects.create_user(username="lewis",phone_number="09134435451", password="testpassword")
        
        self.client = APIClient()
        
        response = self.client.post('/api/user/login/', {'phone_number': '09134435451', 'password': 'testpassword'})
        
        print("Login response status:", response.status_code)
        print("Login response data:", response.data)
        
        self.assertEqual(response.status_code, 200)
        
        self.token = response.json()
        self.assertIn('access_token', self.token, "Access token is not in the response")
        
        self.access_token = self.token['access_token']
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_reservation_success(self):
        data = {
            'book': self.book.bid,
        }
        
        response = self.client.post(
            '/api/book/reserve-book/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.first()
        self.assertEqual(reservation.book, self.book)
        self.assertEqual(reservation.user.phone_number, '09134435451')

        self.book.refresh_from_db()
        self.assertFalse(self.book.availability_status)

    def test_create_reservation_book_not_available(self):
        self.book.availability_status = False
        self.book.save()
        
        data = {
            'book': self.book.bid,
        }
        
        response = self.client.post(
            '/api/book/reserve-book/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data, "Expected 'non_field_errors' key in response")
    
        self.assertEqual(response.data['non_field_errors'][0], 'This book is not available for reservation.')