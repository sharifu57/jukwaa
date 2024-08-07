from rest_framework import serializers
from backend.models import *
from base.models import *
from django.contrib.auth.models import User
from base.serializers import *
import hashlib
from backend.utils import *
from base.serializers import LocationSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = "__all__"


class BidSerializer(serializers.ModelSerializer):
    bidder = UserProfileSerializer()
    class Meta:
        model = Bid
        fields = "__all__"

class DurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duration
        fields = "__all__"


class ProjectsListSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    skills = SkillsSerializer(many=True)
    budget = BudgetSerializer()
    bids = BidSerializer(many=True, read_only=True)
    created_by = UserSerializer()
    category = CategorySerializer()
    # employer = EmployerSerializer()
    encrypted_id = serializers.SerializerMethodField()
    experience = ExperienceSerializer()
    duration = DurationSerializer()

    class Meta:
        model = Project
        fields = "__all__"

    def get_encrypted_id(self, obj):
        """
        This method is called for the `encrypted_id` field.
        """
        return encrypt_id(obj.id)


class BidListSerializer(serializers.ModelSerializer):
    bidder = LoginSerializer()
    project = ProjectSerializer()
    class Meta:
        model = Bid
        fields = "__all__"

    def get_encrypted_id(self, obj):
        """Returns the encrypted ID for the Project instance."""
        return encrypt_id(obj.id)
