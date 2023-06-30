from rest_framework.permissions import BasePermission


class IsOwnerOrIsAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.status == 'DRAFT':
            return request.user == obj.creator
        return request.user == obj.creator or request.user.is_staff
