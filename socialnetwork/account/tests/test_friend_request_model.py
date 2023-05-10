from django.db import IntegrityError
from django.test import TestCase
from account.models import FriendRequest, User


class FriendRequestModelTest(TestCase):
    def setUp(self):
        self.philip = User.objects.create(username='Philip27', password='phtt239Jr@b')
        self.kate = User.objects.create(username='Kate28', password='fk239Jh&re%')
        FriendRequest.objects.create(from_user=self.kate, to_user=self.philip)

    def test_friend_request_fields(self):
        friend_request = FriendRequest.objects.get(id=1)
        self.assertEqual(friend_request.from_user.username, 'Kate28')
        self.assertEqual(friend_request.to_user.username, 'Philip27')

    def test_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            FriendRequest.objects.create(from_user=self.kate, to_user=self.philip)
