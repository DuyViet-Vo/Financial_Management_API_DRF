from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from financial_management.users.models import User
from financial_management.users.serializers import CustomTokenObtainPairSerializer, UserRegistrationSerializer


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["password"] = make_password(serializer.validated_data["password"])
            user = serializer.save()
            return Response(
                {
                    "user": UserRegistrationSerializer(user, context=self.get_serializer_context()).data,
                    "message": "Successful account registration!",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response_data = serializer.validated_data
        return Response(response_data, status=status.HTTP_200_OK)
