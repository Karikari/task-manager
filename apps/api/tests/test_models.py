from datetime import datetime, timedelta
from unittest import TestCase

from faker import Faker

from apps.api.models import Task
from apps.auths.models import User


class TaskTestCase(TestCase):
    def setUp(self):
        """
        Set up test data
        """
        # Create a user for testing
        faker = Faker()
        self.user = User.objects.create_user(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            password='testpassword123'
        )
        # Create a task for testing
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task.',
            status='Pending',
            due_date=datetime.now() + timedelta(days=7),  # Due in 7 days
            assign_to=self.user
        )

    def test_task_creation(self):
      """
      Test that a task is created successfully.
      """
      self.assertEqual(self.task.title, 'Test Task')
      self.assertEqual(self.task.description, 'This is a test task.')
      self.assertEqual(self.task.status, 'Pending')
      self.assertEqual(self.task.assign_to, self.user)
      self.assertTrue(isinstance(self.task.due_date, datetime))

    def test_task_str_method(self):
      """
      Test the __str__ method of the Task model.
      """
      self.assertEqual(str(self.task), 'Test Task')

    def test_task_default_status(self):
        """
        Test that the default status is 'Pending'.
        """
        new_task = Task.objects.create(
            title='Another Task',
            assign_to=self.user
        )
        self.assertEqual(new_task.status, 'Pending')

    def test_task_blank_description(self):
      """
      Test that the description field can be blank.
      """
      new_task = Task.objects.create(
          title='Task with Blank Description',
          assign_to=self.user
      )
      self.assertEqual(new_task.description, '')




