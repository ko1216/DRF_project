from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsModerator(BasePermission):
    """
    This Custom permission class need to use for staff to check safely lessons and courses
    without any permissions to create new or delete one.
    """

    message = 'Вы не являетесь модератором'

    def has_permission(self, request, view) -> bool:
        if request.user.role == UserRoles.moderator:
            return True
        return False


class IsNotModerator(BasePermission):
    """
    This Custom permission class check if user is a moderator to denied permission to create new lesson or course
    """
    def has_permission(self, request, view) -> bool:
        return request.user.role != UserRoles.moderator


class IsCourseOrLessonOwner(BasePermission):
    """
    This Custom permission class need to use for check if user or some member
    is an owner of any courses or lessons to work with it. Member become an owner when he had paid
    for a course or lesson.
    """

    message = 'Вы не являетесь владельцем'

    def has_object_permission(self, request, view, obj: list) -> bool:
        if obj.payments_set.filter(user=request.user).exists():
            return True
        return False
