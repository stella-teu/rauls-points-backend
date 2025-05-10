from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cohort, Profile, PointEvent


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = ['id', 'name']



class PointEventSerializer(serializers.ModelSerializer):
    profile_username = serializers.CharField(source='profile.user.username', read_only=True)
    cohort_name = serializers.CharField(source='profile.cohort.name', read_only=True)

    class Meta:
        model = PointEvent
        fields = ['id', 'value', 'context', 'created_at', 'profile_username', 'cohort_name']


class PointEventWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointEvent
        fields = ['profile', 'value', 'context']



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    cohort_name = serializers.CharField(source='cohort.name', read_only=True)
    total_points = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'cohort_name', 'is_admin', 'total_points']

    def get_total_points(self, obj):
        return obj.pointevent_set.aggregate(total=serializers.Sum('value'))['total'] or 0


class ProfileWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'cohort']