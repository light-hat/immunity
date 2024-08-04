"""
Модульные тесты приложения.
"""

from api.models import User
from django.test import TestCase


class UserModelTest(TestCase):
    """
    Тестовый сценарий для проверки модели пользователя.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), 'testuser')
