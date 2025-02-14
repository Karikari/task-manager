from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.api.models import Task
from apps.auths.models import User


class TaskViewTest(APITestCase):
  def setUp(self):
    """
    Set up test data.
    """
    # Create a user for authentication
    faker = Faker()
    self.user = User.objects.create_user(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
        password='testpassword123'
    )

    # Create some tasks for testing
    self.task1 = Task.objects.create(
        title='Task 1',
        description='Description for Task 1',
        status='Pending',
        assign_to=self.user
    )
    self.task2 = Task.objects.create(
        title='Task 2',
        description='Description for Task 2',
        status='In Progress',
        assign_to=self.user
    )

    # URL for the TaskView
    self.url = reverse('api:tasks')

    # Authenticate the user
    self.client.force_authenticate(user=self.user)


  def test_create_task(self):
    """
    Test creating a new task.
    """
    data = {
      'title': 'New Task',
      'description': 'Description for New Task',
      'status': 'Pending',
      'assign_to': self.user.id
    }

    response = self.client.post(self.url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Verify the task was created in the database
    task = Task.objects.get(title='New Task')
    self.assertEqual(task.description, 'Description for New Task')
    self.assertEqual(task.status, 'Pending')
    self.assertEqual(task.assign_to, self.user)

  def test_create_task_invalid_data(self):
    """
    Test creating a task with invalid data.
    """
    data = {
      'title': '',  # Title is required
      'description': 'Invalid Task',
      'status': 'Pending',
      'assign_to': self.user.id
    }

    response = self.client.post(self.url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_get_all_tasks_unauthenticated(self):
    """
    Test retrieving all tasks without authentication.
    """
    self.client.force_authenticate(user=None)
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_create_task_unauthenticated(self):
    """
    Test creating a task without authentication.
    """
    self.client.force_authenticate(user=None)
    data = {
      'title': 'Unauthenticated Task',
      'description': 'This task should not be created.',
      'status': 'Pending',
      'assign_to': self.user.id
    }

    response = self.client.post(self.url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

