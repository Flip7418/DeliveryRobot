from rest_framework import serializers

from student.models import Student


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    sdu_id = serializers.CharField(source='user.sdu_id', read_only=True)
    iin = serializers.CharField(source='user.iin', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    photo = serializers.ImageField(source='user.photo', read_only=True)
    birth_date = serializers.DateField(source='user.birth_date', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    specialization = serializers.ReadOnlyField(
        source='get_specialization_display')

    class Meta:
        ref_name = 'some'
        model = Student
        fields = ('id', 'sdu_id', 'iin', 'first_name', 'last_name',
                  'photo', 'birth_date', 'phone', 'specialization',
                  'allergy')


class StudentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    photo = serializers.ImageField(source='user.photo', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name',
                  'photo', 'phone')
