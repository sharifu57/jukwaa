from rest_framework import serializers
from base.models import *
from backend.models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Group, User
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "username", "last_name", "email", "password"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"

class UserProfileSerializer(serializers.ModelSerializer):
    # location = LocationSerializer()
    class Meta:
        model = Profile
        fields = "__all__"

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"

class RegisterResponseSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username', 'profile']

class LoginSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Profile
        fields = "__all__"


class VerificationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = "__all__"

class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()
    expires_at = serializers.IntegerField()


# class ProjectSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     location = LocationSerializer()

#     class Meta:
#         model = Project
#         fields = "__all__"

class TeamSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Team
        fields = "__all__"

class EmployersLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ('name', 'company_logo')

class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = "__all__"

class ResetPasswordEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"

class SetNewPasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    uidb64 = serializers.CharField(required=True)

    def validate(self, attrs):
        """
        Here you can add any additional validation you might need.
        For example, checking if the two passwords match.
        """
        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError("The two passwords must match.")

        return attrs

    def save(self, **kwargs):
        """
        Update the user's password.
        """
        user = self.context['user']  # Get the user from the context
        password = self.validated_data['new_password1']
        user.set_password(password)
        user.save()
        return user

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"







