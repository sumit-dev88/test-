from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .models import TaskApi


class TaskApiTestCase(APITestCase):

    # Create a test user and authenticate the API client
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Authenticate all requests by default
        self.client.force_authenticate(user=self.user)

    # Test that an authenticated user can get their tasks
    # Expected response: 200 OK
    def test_get_tasks(self):
        response = self.client.get('/api/tasks/')

        self.assertEqual(response.status_code, 200)

    # Test that an authenticated user can create a task
    # Expected response: 201 Created
    def test_create_task(self):
        data = {
            'title': 'Test Task',
            'description': 'Testing task creation',
            'completed': False
        }

        response = self.client.post('/api/tasks/', data)

        self.assertEqual(response.status_code, 201)

    # Test field-level validation for the title
    # Title must contain at least 3 characters
    # Expected response: 400 Bad Request
    def test_invalid_title(self):
        data = {
            'title': 'ab',
            'description': 'Testing invalid title',
            'completed': False
        }

        response = self.client.post('/api/tasks/', data)

        self.assertEqual(response.status_code, 400)

    # Test that an unauthenticated user cannot access the API
    # Expected response: 401 Unauthorized
    def test_unauthenticated_user(self):
        self.client.force_authenticate(user=None)

        response = self.client.get('/api/tasks/')

        self.assertEqual(response.status_code, 401)

    # Test that a non-existing task returns 404
    # Expected response: 404 Not Found
    def test_task_not_found(self):
        response = self.client.get('/api/tasks/9999/')

        self.assertEqual(response.status_code, 404)

    # Test that an admin user can delete a task
    # Expected response: 204 No Content
    def test_delete_task(self):
        task = TaskApi.objects.create(
            title='Delete Task',
            description='Testing delete',
            completed=False,
            user=self.user
        )

        # Make the test user an admin/staff user
        self.user.is_staff = True
        self.user.save()

        response = self.client.delete(f'/api/tasks/{task.id}/')

        self.assertEqual(response.status_code, 204)

    # Test that an authenticated user can update a task
    # Expected response: 200 OK
    def test_update_task(self):
        task = TaskApi.objects.create(
            title='Old Title',
            description='Old Description',
            completed=False,
            user=self.user
        )

        response = self.client.patch(
            f'/api/tasks/{task.id}/',
            {'title': 'Updated Title'}
        )

        self.assertEqual(response.status_code, 200)

        # Verify that the title was actually updated
        self.assertEqual(response.data['title'], 'Updated Title')

    # Test that a user cannot access another user's task
    # Expected response: 404 Not Found
    def test_user_cannot_access_other_user_task(self):
        task = TaskApi.objects.create(
            title='Private Task',
            description='User A task',
            completed=False,
            user=self.user
        )

        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )

        # Authenticate as the second user
        self.client.force_authenticate(user=other_user)

        response = self.client.get(f'/api/tasks/{task.id}/')

        self.assertEqual(response.status_code, 404)

    # Test object-level validation
    # A completed task must have a description
    # Expected response: 400 Bad Request
    def test_completed_task_requires_description(self):
        data = {
            'title': 'Completed Task',
            'description': '',
            'completed': True
        }

        response = self.client.post('/api/tasks/', data)

        self.assertEqual(response.status_code, 400)

