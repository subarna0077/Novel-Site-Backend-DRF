from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user

class IsNovelOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.author == request.user
    
class IsCommentOwnerOrAuthorOrReadOnly(BasePermission):   
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        user = request.user
        ## think of the code below as a guard block
        ## if the user is unauthenticated, then immediately deny permissions
        ## returning false immediately blocks all the write operations for the unauthenticateed users
        if not request.user or not request.user.is_authenticated:
            return False
        
        return (
            obj.user_id == user.id or
            obj.novel.author_id == user.id or
            user.is_staff
        )