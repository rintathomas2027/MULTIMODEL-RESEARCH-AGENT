from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['research_interests', 'academic_level', 'avatar', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

    def get_profile(self, obj):
        profile, created = UserProfile.objects.get_or_create(user=obj)
        return UserProfileSerializer(profile).data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)
    email = serializers.EmailField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    research_interests = serializers.CharField(write_only=True, required=False, allow_blank=True)
    academic_level = serializers.CharField(write_only=True, required=False, default='MCA Student')
    avatar = serializers.CharField(write_only=True, required=False, default='technomancer')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'research_interests', 'academic_level', 'avatar']

    def create(self, validated_data):
        interests = validated_data.pop('research_interests', '')
        level = validated_data.pop('academic_level', 'MCA Student')
        avatar_val = validated_data.pop('avatar', 'technomancer')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.research_interests = interests
        profile.academic_level = level
        profile.avatar = avatar_val
        profile.save()
        
        return user
