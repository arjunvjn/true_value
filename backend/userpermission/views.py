from rest_framework import permissions
from django.contrib.auth.models import User

# Create your views here.

class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            member=User.objects.get(username=request.user.username)
            return (request.user.is_staff or (member and request.method=='DELETE'))
        except:
            pass

class BookPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            member=User.objects.get(username=request.user.username)
            return (request.user.is_staff or (member and (request.method=='GET' or request.method=='PATCH')))
        except:
            pass