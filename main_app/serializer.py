from rest_framework import serializers
from .models import Cohort, Profile, PointEvent

class CohortSerializer(serializers.ModelSerializer):
    class Meta :
        model = Cohort
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta :
        model = Profile
        fields = '__all__'

class PointEventSerializer(serializers.ModelSerializer):
    class Meta :
        model = PointEvent
        fields = '__all__'