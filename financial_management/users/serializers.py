from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ParseError

from financial_management.core.custom_parse_errors import CustomParseError
from financial_management.users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "phone", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def to_internal_value(self, data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        phone = data.get("phone")
        if username == "":
            raise CustomParseError(1000, "Username cannot be left blank!")
        if email == "":
            raise CustomParseError(1000, "Email cannot be left blank!")
        if password == "":
            raise CustomParseError(1001, "Password cannot be left blank!")

        if phone == "":
            raise CustomParseError(9021, "Phone cannot be left blank!")
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise CustomParseError(9022, "Invalid email!")

        return super().to_internal_value(data)

    def validate_phone(self, value):
        if not value.isdigit():
            raise CustomParseError(9023, "The phone number must contain all numbers")
        if not value.startswith("0"):
            raise CustomParseError(9024, "Phone numbers must start with 0")

        if User.objects.filter(phone=value).exists():
            raise CustomParseError(9010, "This phone number already exists!")
        if not (10 <= len(value) <= 11):
            raise CustomParseError(9011, "Phone number must be 10 or 11 digits!")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise CustomParseError(9012, "This email already exists!")
        return value

    def validate_password(self, value):
        if not (len(value) >= 6):
            raise CustomParseError(9013, "Password must be over 6 characters!")
        return value
