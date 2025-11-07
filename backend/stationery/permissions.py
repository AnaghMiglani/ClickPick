"""
Custom permission classes for stationery app
"""
from rest_framework import permissions


class IsAdminOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow users with ADMIN or STAFF role.
    This is for admin panel endpoints that need elevated permissions.
    """
    
    def has_permission(self, request, view):
        # User must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # User must have ADMIN or STAFF role
        return request.user.role in ['ADMIN', 'STAFF']


class IsStudent(permissions.BasePermission):
    """
    Custom permission to only allow users with STUDENT role.
    This is for student-facing mobile app endpoints.
    """
    
    def has_permission(self, request, view):
        # User must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # User must have STUDENT role
        return request.user.role == 'STUDENT'
