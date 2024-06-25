from rest_framework import serializers

from financial_management.groups.models import Group
from financial_management.users.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class ReadGroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Group
        fields = ("id", "name", "owner", "created_at")
