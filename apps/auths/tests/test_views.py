from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.auths.models import User


class SignUpViewTest(APITestCase):
    def setUp(self):
        faker = Faker()
        """
        Set up test data.
        """
        self.url = "/api/signup"
        self.valid_data = {
            'email': faker.email(),
            'password': 'testpassword123',
            'first_name': faker.first_name(),
            'last_name': faker.last_name(),
        }
        self.invalid_data = {
            'email': 'invalid-email',
            'password': 'testpassword123',
        }
    def tearDown(self):
        User.objects.all().delete()

    def test_signup_with_valid_data(self):
        """
        Test signing up with valid data.
        """
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', response.data)
        self.assertIn('token', response.data)

        # Verify the user was created in the database
        user = User.objects.get(email=self.valid_data['email'])
        self.assertEqual(user.email, self.valid_data['email'])

    def test_signup_with_existing_user(self):
        """
        Test signing up with an existing user email.
        """
        # Create a user with the same email
        User.objects.create_user(
            first_name=self.valid_data['first_name'],
            last_name=self.valid_data['last_name'],
            email=self.valid_data['email'],
            password=self.valid_data['password'],
        )

        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'User already exist')

    def test_signup_with_invalid_data(self):
        """
        Test signing up with invalid data.
        """
        response = self.client.post(self.url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class LoginViewTest(APITestCase):
    def setUp(self):
        """
        Set up test data.
        """
        faker = Faker()
        email = faker.email()
        self.url = "/api/login"
        self.user = User.objects.create_user(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=email,
            password='testpassword123',
        )
        self.valid_data = {
            'email': email,
            'password': 'testpassword123',
        }
        self.invalid_data = {
            'email': email,
            'password': 'wrongpassword',
        }

    def test_login_with_valid_credentials(self):
        """
        Test logging in with valid credentials.
        """
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_with_invalid_credentials(self):
        """
        Test logging in with invalid credentials.
        """
        response = self.client.post(self.url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_login_with_nonexistent_user(self):
        """
        Test logging in with a nonexistent user.
        """
        nonexistent_data = {
            'email': 'nonexistent@example.com',
            'password': 'testpassword123',
        }
        response = self.client.post(self.url, nonexistent_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)