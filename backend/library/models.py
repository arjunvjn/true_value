from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    name=models.CharField(max_length=50,unique=True)
    author=models.CharField(max_length=50)
    status=models.CharField(default='AVAILABLE',max_length=25)

    def __str__(self):
        return self.name
        
class BorrowedBooks(models.Model):
    member=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.OneToOneField(Book,on_delete=models.CASCADE)

    def __str__(self):
        return self.book.name