from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    """
    Allows access only to students.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_student)


class IsDoctor(BasePermission):
    """
    Allows access only to doctors.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_doctor)
