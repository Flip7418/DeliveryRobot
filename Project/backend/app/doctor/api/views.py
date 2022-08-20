from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authorization.permissions import IsDoctor
from doctor.api.serializers import ProfileSerializer
from user.api.serializers import UserUpdateSerializer


class ProfileViewSet(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsDoctor)
    serializer_class = ProfileSerializer
    user_serializer_class = UserUpdateSerializer

    def get(self, request, *args, **kwargs):
        user = request.user

        return Response(
            self.serializer_class(user.doctor).data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, *args, **kwargs):
        user = request.user

        updated_user = self.user_serializer_class(user, data=request.data)
        assert updated_user.is_valid(raise_exception=True)
        user = updated_user.save()

        return Response(
            data=self.serializer_class(user.doctor).data,
            status=status.HTTP_200_OK,
        )
