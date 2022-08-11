from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Book,BorrowedBooks
from .serializer import MyTokenObtainPairSerializer,RegisterSerializer,UserSerializer,BookSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from userpermission.views import UserPermission,BookPermission

# Create your views here.

'''
Function to delete members and to set status of books, 
that are borrowed by that member, to available
'''
def check_book(user):
    if BorrowedBooks.objects.filter(member=user).exists():
        for i in BorrowedBooks.objects.filter(member=user):
            book=Book.objects.get(pk=i.book.id)
            book.status='AVAILABLE'
            book.save()

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class UserDetails(APIView):
    permission_classes = [UserPermission]

    # To get list of members for the librarian
    def get(self,request):
        members=User.objects.filter(is_staff=False)
        serializer=UserSerializer(members,many=True)
        return Response(serializer.data)
    
    # For librarian to add members
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Member Created'})
        else:
            return Response({'msg':serializer.errors})

    # For librarian to update members
    def put(self,request):
        id=int(request.GET.get('id'))
        member=User.objects.get(pk=id)
        serializer=UserSerializer(member,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Member Details Updated'})
        else:
            return Response({'msg':serializer.errors})

    '''
    For librarian to remove an member or 
    for a member to delete his own account.
    '''
    def delete(self,request):
        id=int(request.GET.get('id'))
        if request.user.is_staff:
            try:
                user=User.objects.get(pk=id)
                check_book(user)
                User.objects.filter(pk=id).delete()
                return Response({'msg':'Member Deleted'})
            except:
                return Response({'msg':'Member Not Found'})
        else:
            if request.user.id==id:
                if BorrowedBooks.objects.filter(member=request.user).exists():
                    return Response({'msg':'You need to return the books before deleting your account'})
                else:
                    User.objects.filter(pk=id).delete()
                    return Response({'msg':'Account Deleted'})
            else:
                return Response({'msg':'Not Authorized'})
        
class BookDetails(APIView):
    permission_classes = [BookPermission]

    # To list all books
    def get(self,request):
        books=Book.objects.all()
        serializer=BookSerializer(books,many=True)
        return Response(serializer.data)

    # For librarian to create an book
    def post(self,request):
        serializer=BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Book Added'})
        else:
            return Response({'msg':serializer.errors})

    # For librarian to update a book
    def put(self,request):
        id=int(request.GET.get('id'))
        book=Book.objects.get(pk=id)
        serializer=BookSerializer(book,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Book Details Updated'})
        else:
            return Response({'msg':serializer.errors})

    '''
    To change the status of book as 'BORROWED' or 'AVAILABLE' 
    when a member borrows or returns the book.
    '''
    def patch(self,request):
        id=int(request.GET.get('id'))
        book=Book.objects.get(pk=id)
        if book.status=='AVAILABLE':
            book.status='BORROWED'
            book.save()
            BorrowedBooks.objects.create(book=book,member=request.user)
            return Response({'msg':'Book Borrowed'})
        elif BorrowedBooks.objects.filter(book=book,member=request.user).exists():
            book.status='AVAILABLE'
            book.save()
            BorrowedBooks.objects.filter(book=book,member=request.user).delete()
            return Response({'msg':'Book Returned'})
        else:
            return Response({'msg':'Book is Borrowed by another person'})

    # For librarian to delete a book
    def delete(self,request):
        id=int(request.GET.get('id'))
        try:
            Book.objects.filter(pk=id).delete()
            return Response({'msg':'Book Removed'})
        except:
            return Response({'msg':'Book Not Found'})