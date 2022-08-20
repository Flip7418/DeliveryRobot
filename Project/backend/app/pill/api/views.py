from rest_framework import mixins
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from pill.api.serializers import BodyPartSerializer, SimptomSerializer, \
    PillSerializer
from pill.models import BodyPart, Simptom, Pill


class BodyPartViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = BodyPart.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = BodyPartSerializer
