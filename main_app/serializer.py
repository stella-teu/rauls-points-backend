from rest_framework import serializers
from django.db.models import Sum
from django.contrib.auth.models import User
from .models import Cohort, Profile, PointEvent


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
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
        # Use annotation if it exists
        if hasattr(obj, 'total_points_agg') and obj.total_points_agg is not None:
            return obj.total_points_agg
        # Fall back to model method if no annotation
        return obj.total_points()
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('User', None)
        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.save()
        return super().update(instance, validated_data)

class PointEventSerializer(serializers.ModelSerializer):
    profile_username = serializers.CharField(source='profile.user.username', read_only=True)
    # cohort_name = serializers.CharField(source='profile.cohort.name', read_only=True)

    class Meta:
        model = PointEvent
        fields = ['id', 'value', 'context', 'created_at', 'profile_username']
