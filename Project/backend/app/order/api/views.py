from rest_framework import mixins, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from authorization.permissions import IsStudent, IsDoctor
from order.api.serializers import OrderSerializer, OrderCreateSerializer, \
    DoctorOrderSerializer, DeclineOrderSerializer, ApproveOrderSerializer, \
    OrderDecisionResponseSerializer, OrderShortSerializer, \
    OrderDecisionPillCreateSerializer
from order.constants import ActiveStatuses, FinishedStatuses, \
    OrderModerationType, OrderDeclinedType, OrderApprovedType, \
    OrderAtClientType, OrderDeliveredType, PointSourceType
from order.models import Order
from order.tasks import notify_robot


class OrderStatusFilterBackend(filters.BaseFilterBackend):
    """
    Custom status filter for student, doctor orders
    """

    def filter_queryset(self, request, queryset, view):
        state = request.query_params.get('state', None)
        if state:
            if state == 'active':
                return queryset.filter(status__in=ActiveStatuses)
            elif state == 'finished':
                return queryset.filter(status__in=FinishedStatuses)
        return queryset


class StudentOrderViewSet(GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin):
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = OrderSerializer
    filter_backends = [OrderStatusFilterBackend]

    def get_serializer_class(self):
        if self.action in ['create']:
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(student_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.perform_create(serializer)

        read_serializer = OrderSerializer(order)
        headers = self.get_success_headers(read_serializer.data)

        return Response(read_serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    @action(methods=['get'], detail=True,
            serializer_class=None)
    def received(self, request, *args, **kwargs):
        instance = self.get_object()
        student = request.user.student

        if instance.student.pk != student.pk or \
                instance.status != OrderAtClientType:
            return Response(status=status.HTTP_403_FORBIDDEN)

        notify_robot(instance, PointSourceType)

        instance.status = OrderDeliveredType
        instance.save()

        order_serializer = OrderShortSerializer(instance)
        return Response(order_serializer.data, status=status.HTTP_200_OK)


class DoctorOrderViewSet(GenericViewSet,
                         mixins.ListModelMixin):
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated, IsDoctor)
    serializer_class = DoctorOrderSerializer
    filter_backends = [OrderStatusFilterBackend]

    @action(methods=['post'], detail=True,
            serializer_class=DeclineOrderSerializer)
    def decline(self, request, *args, **kwargs):
        instance = self.get_object()
        doctor = request.user.doctor

        if instance.status != OrderModerationType:
            return Response(status=status.HTTP_403_FORBIDDEN)

        decision = DeclineOrderSerializer(data=request.data)
        decision.is_valid(raise_exception=True)
        decision = decision.save(doctor=doctor, order=instance)

        instance.status = OrderDeclinedType
        instance.save()

        decision_serializer = OrderDecisionResponseSerializer(decision)
        return Response(decision_serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True,
            serializer_class=OrderDecisionPillCreateSerializer)
    def approve(self, request, *args, **kwargs):
        instance = self.get_object()
        doctor = request.user.doctor

        if instance.status != OrderModerationType:
            return Response(status=status.HTTP_403_FORBIDDEN)

        decision = ApproveOrderSerializer(data=request.data)
        decision.is_valid(raise_exception=True)
        decision = decision.save(doctor=doctor, order=instance)

        instance.status = OrderApprovedType
        instance.save()

        decision_serializer = OrderDecisionResponseSerializer(decision)
        return Response(decision_serializer.data, status=status.HTTP_200_OK)
