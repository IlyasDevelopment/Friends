from django.test import TestCase
from account.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='Leonid29', password='11$2lI3jH')

    def test_user_fields(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.username, 'Leonid29')
        self.assertEqual(user.password, '11$2lI3jH')

    def test_username_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('username').max_length
        self.assertEqual(max_length, 150)

    def test_get_absolute_url(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.get_absolute_url(), '/account/users/Leonid29/')
