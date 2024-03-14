from rest_framework import serializers
from base.models import *
from backend.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "username", "last_name", "email", "password"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
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


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
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

class SetNewPasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    uidb64 = serializers.CharField(required=True)

    def validate(self, attrs):
        self.user = self.context['request'].user
        # Add your validation for token and uid here if needed
        return attrs

    def save(self):
        password = self.validated_data['new_password1']
        user = self.user
        user.set_password(password)
        user.save()






