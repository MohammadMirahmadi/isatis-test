ابتدا محیط مجازی را ساخته و فعال کنید.
دستور pip install -r requirements.txt را وارد کنید.
دستور python manage.py makemigrations را وارد کنید.
دستور python manage.py migrate را وارد کنید.

یک unit test نوشته شده است برای رزرو کتاب که با دستور: python manage.py test book کار میکند.
در بخش middleware، یک middleware نوشته شده برای ثبت لاگ ها که در request_response.log ذخیره میشود.
برای url های /api/book/reserve-book/ و /api/book/book-detail/ محدودیت تعداد درخواست در دقیقه لحاظ شده است.
برای ساخت superuser علاوه بر آدرس /api/user/create-superuser/ ، با دستور کاستوم شده python manage.py create_superuser هم میتوان superuser ساخت.
برای توضیحات هم با swagger با آدرس /api/swagger-custom/ ، توضیحات قابل دریافت است.
پنل ادمین هم با آدرس /api/admin/ در دسترس است.
