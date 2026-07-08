from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone
from datetime import timedelta

class IsAuth(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsAnon(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class CanEditWithIn15Minutes(BasePermission):

    def has_object_permission(self, request, view, obj):
        time_passed = timezone.now() - obj.created_at
        return time_passed <= timedelta(minutes=45)
    
class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff and request.method in ('GET','PUT','PATCH','DELETE')
