from rest_framework import permissions
from rest_framework.permissions import BasePermission


# GET:누구나, PUT/PATCH: 해당 프로필 유저
class CustomReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # GET 요청
            return True
        return obj.user == request.user # PUT/PATCH 요청