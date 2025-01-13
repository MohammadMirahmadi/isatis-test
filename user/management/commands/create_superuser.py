from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

# اسکریپت اختصاصی برای ساخت سوپریوزر(python manage.py create_superuser)
class Command(BaseCommand):
    help = 'Create a superuser with additional fields'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")
        name = input("Name: ")
        national_code = input("National Code: ")
        phone_number = input("Phone Number: ")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists'))
            return
        if User.objects.filter(phone_number=phone_number).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists'))
            return
        if User.objects.filter(national_code=national_code).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists'))
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            name=name,
            national_code=national_code,
            phone_number=phone_number
        )

        self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully'))
