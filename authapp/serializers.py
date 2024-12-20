from rest_framework import serializers
from .models import User,Profile,TutorProfile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number', 'profile_image', 'qualification']
        

class TutorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorProfile
        fields = ["qualification", "bio", "experience", "profile_image"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'profile']

    def update(self, instance, validated_data):
        # Pop the nested profile data
        profile_data = validated_data.pop('profile', None)

        # Update the User model
        instance = super().update(instance, validated_data)

        if profile_data:
            # Ensure profile data is updated or created
            Profile.objects.update_or_create(user=instance, defaults=profile_data)

        return instance




class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_active','document_tutor']

class TutorSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role','document_tutor')

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['role'] = 'tutor'  # Default role as tutor
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

