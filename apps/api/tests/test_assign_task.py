from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.api.models import Task, TaskComment

User = get_user_model()

class AssignTaskViewTests(APITestCase):
    def setUp(self):
        """Set up test data and authenticate user."""
        faker = Faker()
        self.user = User.objects.create_user(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            password="password123"
        )
        self.another_user = User.objects.create_user(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            password="password123"
        )

        self.task = Task.objects.create(title="Test Task", description="Task description", assign_to=self.user)

        self.assign_task_url = "/api/tasks/{}/assign/{}".format(self.task.id, str(self.user.id))

        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        """Clean up database after each test."""
        Task.objects.all().delete()
        User.objects.all().delete()

    def test_assign_task_success(self):
        """Test assigning a task successfully."""
        response = self.client.get(self.assign_task_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.assign_to, self.user)

    def test_assign_task_not_found(self):
        """Test assigning a task that doesn't exist."""
        invalid_task_url = "/api/tasks/{}/assign/{}".format("999", str(self.user.id))  # Invalid task ID
        response = self.client.get(invalid_task_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_assign_task_user_not_found(self):
        """Test assigning a task to a non-existent user."""
        invalid_user_url = "/api/tasks/{}/assign/999".format(str(self.task.id))  # Invalid user ID
        response = self.client.get(invalid_user_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentsAPIViewTests(APITestCase):
    def setUp(self):
        """Set up test data and authenticate user."""
        faker = Faker()
        self.user = User.objects.create_user(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            password="password123"
        )

        self.task = Task.objects.create(
            title="Test Task",
            description="Task description",
            assign_to=self.user
        )

        self.comment_url = "/api/tasks/{}/comments".format(self.task.id)

        self.client.force_authenticate(user=self.user)

    def tearDown(self):
      Task.objects.all().delete()
      User.objects.all().delete()
      TaskComment.objects.all().delete()

    def test_get_comments_success(self):
        """Test retrieving comments for a task."""
        TaskComment.objects.create(task=self.task, user=self.user, comment="Test Comment")

        response = self.client.get(self.comment_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["comment"], "Test Comment")

    def test_add_comment_success(self):
        """Test adding a comment successfully."""
        comment_data = {"comment": "New comment"}

        response = self.client.post(self.comment_url, comment_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"], "New comment")

        # Ensure comment is saved in DB
        self.assertEqual(TaskComment.objects.count(), 1)
        self.assertEqual(TaskComment.objects.first().comment, "New comment")

    def test_add_comment_task_not_found(self):
        """Test adding a comment to a non-existent task."""
        invalid_comment_url = "/api/tasks/999/comments/"
        comment_data = {"comment": "New comment"}

        response = self.client.post(invalid_comment_url, comment_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_comment_empty_comment(self):
        """Test adding an empty comment (should fail)."""
        comment_data = {"comment": ""}

        response = self.client.post(self.comment_url, comment_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


