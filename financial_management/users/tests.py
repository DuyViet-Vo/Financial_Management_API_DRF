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


class LoginTests(APITestCase):
    def setUp(self):
        # Tạo một user để test
        self.test_user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword", phone="1234567890"
        )

        # URL cho API login
        self.login_url = reverse("login")  # Giả sử 'login' là tên của url pattern cho API login

    def test_login_successful(self):
        """
        Đảm bảo chúng ta có thể đăng nhập thành công với email và password đúng.
        """
        data = {"email": "test@example.com", "password": "testpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)  # Giả sử API trả về một token

    def test_login_failed_wrong_password(self):
        """
        Đảm bảo đăng nhập thất bại với mật khẩu sai.
        """
        data = {"email": "test@example.com", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_failed_email_not_exist(self):
        """
        Đảm bảo đăng nhập thất bại với email không tồn tại.
        """
        data = {"email": "nonexistent@example.com", "password": "testpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_email(self):
        """
        Đảm bảo API xử lý đúng khi thiếu email trong request.
        """
        data = {"password": "testpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_password(self):
        """
        Đảm bảo API xử lý đúng khi thiếu password trong request.
        """
        data = {"email": "test@example.com"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
