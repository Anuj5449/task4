from rest_framework import permissions


class IsOwnerAuthenticated(permissions.BasePermission):
    def  has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return(request.user == obj.created_by)