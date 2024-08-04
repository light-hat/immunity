"""
Модульные тесты приложения.
"""

from django.test import TestCase

from .models import CustomUser


class CustomUserModelTest(TestCase):
    """
    Тестовый сценарий для проверки модели пользователя.
    """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
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
