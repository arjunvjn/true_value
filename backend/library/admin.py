from django.contrib import admin
from .models import Book,BorrowedBooks

# Register your models here.

admin.site.register(Book)
admin.site.register(BorrowedBooks)