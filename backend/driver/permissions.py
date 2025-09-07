from rest_framework.permissions import BasePermission

class IsDriver(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_driver
    
class IsAvailableDriver(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_driver and request.user.driverprofile.is_available

class IsVerifiedDriver(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_driver and request.user.driverprofile.is_verified