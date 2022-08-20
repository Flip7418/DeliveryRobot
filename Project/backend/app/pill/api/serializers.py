from rest_framework import serializers

from pill.models import BodyPart, Simptom, Pill, Text


class TextPillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Text
        fields = ('id', 'pharmacotherapeutic_group', 'description',
                  'indication', 'application_method')


class PillSerializer(serializers.ModelSerializer):
    text = TextPillSerializer()
    class Meta:
        model = Pill
        fields = ('id', 'title', 'photo', 'description', 'text')


class SimptomSerializer(serializers.ModelSerializer):
    pills = PillSerializer(many=True)

    class Meta:
        model = Simptom
        fields = ('id', 'title', 'pills', )


class BodyPartSerializer(serializers.ModelSerializer):
    simptoms = SimptomSerializer(many=True)

    class Meta:
        model = BodyPart
        fields = ('id', 'title', 'simptoms', )
