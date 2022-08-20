from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authorization.permissions import IsStudent
from student.api.serializers import ProfileSerializer
from user.api.serializers import UserUpdateSerializer


class ProfileViewSet(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = ProfileSerializer
    user_serializer_class = UserUpdateSerializer

    def get(self, request, *args, **kwargs):
        user = request.user

        return Response(
            self.serializer_class(user.student).data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, *args, **kwargs):
        user = request.user

        updated_user = self.user_serializer_class(user, data=request.data)
        assert updated_user.is_valid(raise_exception=True)
        updated_user.save()

        updated_student = self.serializer_class(user.student,
                                                data=request.data)
        assert updated_student.is_valid(raise_exception=True)
        student = updated_student.save()

        return Response(
            data=self.serializer_class(student).data,
            status=status.HTTP_200_OK,
        )
