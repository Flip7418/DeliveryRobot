from rest_framework import serializers

from doctor.api.serializers import DoctorSerializer
from order.models import Order, OrderSimptom, OrderPill, OrderDecisionPill, \
    OrderDecision
from student.api.serializers import StudentSerializer


class OrderSimptomSerializer(serializers.ModelSerializer):
    simptom = serializers.SlugField()

    class Meta:
        model = OrderSimptom
        fields = ('simptom', )


class OrderSimptomCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderSimptom
        fields = ('simptom', )


class OrderPillSerializer(serializers.ModelSerializer):
    pill = serializers.SlugField()

    class Meta:
        model = OrderPill
        fields = ('pill', 'count')


class OrderPillCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderPill
        fields = ('pill', 'count', )


class OrderDecisionPillSerializer(serializers.ModelSerializer):
    pill = serializers.SlugField()

    class Meta:
        model = OrderDecisionPill
        fields = ('pill', 'count', )


class OrderShortSerializer(serializers.ModelSerializer):
    destination = serializers.SlugField()

    class Meta:
        model = Order
        fields = ('id', 'order_type', 'created_at', 'destination',
                  'description', 'status')


class OrderSerializer(serializers.ModelSerializer):
    destination = serializers.SlugField()
    requested_simptoms = OrderSimptomSerializer(source='order_simptoms',
                                                many=True)
    requested_pills = OrderPillSerializer(source='order_pills', many=True)
    doctor = DoctorSerializer(source='order_decision.doctor')
    decline_reason = serializers.CharField(
        source='order_decision.decline_reason')
    accepted_pills = OrderDecisionPillSerializer(
        source='order_decision.pills', many=True)

    class Meta:
        model = Order
        fields = ('id', 'order_type', 'created_at', 'destination',
                  'description', 'status', 'requested_simptoms',
                  'requested_pills', 'doctor', 'decline_reason',
                  'accepted_pills')


class OrderCreateSerializer(serializers.ModelSerializer):
    pills = OrderPillCreateSerializer(many=True)
    simptoms = OrderSimptomCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ('order_type', 'description', 'pills', 'simptoms', )

    def create(self, validated_data):
        pills = validated_data.pop('pills')
        simptoms = validated_data.pop('simptoms')

        order = Order.objects.create(student=self.context[
            "request"].user.student, **validated_data)

        order_pills = []
        for order_pill in pills:
            order_pills.append(OrderPill(
                pill=order_pill['pill'],
                count=order_pill['count'],
                order=order
            ))
        OrderPill.objects.bulk_create(order_pills)

        order_simptoms = []
        for order_simptom in simptoms:
            order_simptoms.append(OrderSimptom(
                simptom=order_simptom['simptom'],
                order=order
            ))
        OrderSimptom.objects.bulk_create(order_simptoms)

        return order


class DoctorOrderSerializer(OrderSerializer):
    student = StudentSerializer()

    class Meta:
        model = Order
        fields = OrderSerializer.Meta.fields + (
            'student',
        )


class OrderDecisionResponseSerializer(serializers.ModelSerializer):
    order = OrderShortSerializer()
    doctor = DoctorSerializer()
    pills = OrderDecisionPillSerializer(many=True)

    class Meta:
        model = OrderDecision
        fields = ('order', 'doctor', 'decline_reason', 'pills', )


class DeclineOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDecision
        fields = ('decline_reason', )


class OrderDecisionPillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDecisionPill
        fields = ('pill', 'count', )


class ApproveOrderSerializer(serializers.ModelSerializer):
    pills = OrderDecisionPillCreateSerializer(many=True)

    class Meta:
        model = OrderDecision
        fields = ('pills', )

    def create(self, validated_data):
        pills = validated_data.pop('pills')

        decision = OrderDecision.objects.create(**validated_data)

        order_decision_pills = []
        for order_decision_pill in pills:
            order_decision_pills.append(OrderDecisionPill(
                pill=order_decision_pill['pill'],
                count=order_decision_pill['count'],
                order_decision=decision
            ))
        OrderDecisionPill.objects.bulk_create(order_decision_pills)

        return decision
