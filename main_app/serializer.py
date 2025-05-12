from rest_framework import serializers
from django.db.models import Sum
from django.contrib.auth.models import User
from .models import Cohort, Profile, PointEvent


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user

class CohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = ['id', 'name']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    cohort_name = serializers.CharField(source='cohort.name', read_only=True)
    total_points = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_total_points(self, obj):
        return obj.pointevent_set.aggregate(total=Sum('value'))['total'] or 0


# class ProfileWriteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['bio', 'cohort']

class PointEventSerializer(serializers.ModelSerializer):
    profile_username = serializers.CharField(source='profile.user.username', read_only=True)
    # cohort_name = serializers.CharField(source='profile.cohort.name', read_only=True)

    class Meta:
        model = PointEvent
        fields = ['id', 'value', 'context', 'created_at', 'profile_username']

# class PointEventWriteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PointEvent
#         fields = ['profile', 'value', 'context']