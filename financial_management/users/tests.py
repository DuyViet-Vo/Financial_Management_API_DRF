from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from financial_management.users.models import User


class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("register")
        self.user_data = {
            "username": "testuser",
            "password": "testpassword123",
            "phone": "0123456789",
            "email": "testuser@example.com",
        }

    def test_user_registration(self):
        response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")

    def test_user_registration_with_existing_email(self):
        self.client.post(self.url, self.user_data, format="json")
        response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_user_registration_missing_fields(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_invalid_email(self):
        invalid_data = self.user_data.copy()
        invalid_data["email"] = "invalidemail"
        response = self.client.post(self.url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_phone_number_format(self):
        # Kiểm tra số điện thoại phải là số
        self.user_data["phone"] = "abcdefghij"
        response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_phone_number_length(self):
        # Kiểm tra số điện thoại có độ dài là 10 hoặc 11
        self.user_data["phone"] = "012345678"
        response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.user_data["phone"] = "01234567890"
        response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_phone_number_start_with_zero(self):
        # Kiểm tra số điện thoại bắt đầu bằng số 0
        self.user_data["phone"] = "9123456789"
        response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.user_data["phone"] = "0123456789"
        response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
