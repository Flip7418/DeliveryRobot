from rest_framework import serializers

from user.models import User


class LoginSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    sdu_id = serializers.CharField(max_length=128)
    iin = serializers.CharField(max_length=52)
    token = serializers.CharField(max_length=256, read_only=True)

    def validate(self, data):
        sdu_id = data.get('sdu_id', None)
        iin = data.get('iin', None)

        user = User.objects.filter(sdu_id=sdu_id, iin=iin).first()

        if user is None:
            raise serializers.ValidationError(
                'A user with this sdu_id and iin is not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'sdu_id': user.sdu_id,
            'iin': user.iin,
            'token': user.token
        }
