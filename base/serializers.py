from rest_framework import serializers
from base.models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "username", "last_name", "email", "password"]