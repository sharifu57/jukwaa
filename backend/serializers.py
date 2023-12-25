from rest_framework import serializers
from backend.models import Project


class ProjectSerializer(serializers.Serializer):
    class Meta:
        model = Project
        fields = "__all__"
