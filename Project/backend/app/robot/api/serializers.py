from rest_framework import serializers
from robot.models import Robot


class RobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = ('title', 'is_active', 'is_available', )

