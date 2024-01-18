from rest_framework import serializers
from backend.models import *
from base.models import *
from django.contrib.auth.models import User
from base.serializers import *


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
    class Meta:
        model = Bid
        fields = "__all__"

class ProjectsListSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    skills = SkillsSerializer(many=True)
    budget = BudgetSerializer()
    bids = BidSerializer(many=True, read_only=True)
    created_by = UserSerializer()
    category = CategorySerializer()

    class Meta:
        model = Project
        fields = "__all__"

class BidListSerializer(serializers.ModelSerializer):
    bidder = LoginSerializer()
    project = ProjectSerializer()
    class Meta:
        model = Bid
        fields = "__all__"
