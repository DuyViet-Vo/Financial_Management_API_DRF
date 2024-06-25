from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from financial_management.groups.models import Group
from financial_management.groups.serializers import GroupSerializer, ReadGroupSerializer


class ListCreateGroupView(ListCreateAPIView):
    model = Group
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadGroupSerializer
        return GroupSerializer


class UpdateDeleteGroupView(RetrieveUpdateDestroyAPIView):
    model = Group
    lookup_field = "id"
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadGroupSerializer
        return GroupSerializer
