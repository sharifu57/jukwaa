from rest_framework import serializers
from backend.models import *
from base.models import *


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
    skills = SkillsSerializer(many=True)
    budget = BudgetSerializer()
    bids = BidSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
