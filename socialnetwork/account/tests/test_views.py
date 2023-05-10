from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from account.models import User, FriendRequest


class ViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='testpass1')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        self.user3 = User.objects.create_user(username='testuser3', password='testpass3')

    def test_user_list_view_uses_correct_template(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/user/list.html')

    def test_request_list_view_uses_correct_template(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse('request_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/user/friend_requests.html')

    def test_accept_friend_request(self):
        self.client.force_login(self.user1)
        friend_request = FriendRequest.objects.create(from_user=self.user2, to_user=self.user1)
        response = self.client.post(reverse('accept_friend_request', args=[self.user2.username]))
        self.assertRedirects(response, reverse('request_list'))
        self.assertFalse(FriendRequest.objects.filter(id=friend_request.id).exists())
        self.assertTrue(self.user1.friends.filter(id=self.user2.id).exists())
        self.assertTrue(self.user2.friends.filter(id=self.user1.id).exists())

    def test_send_friend_request(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('send_friend_request', args=[self.user2.username]))
        self.assertRedirects(response, reverse('user_detail', args=[self.user2.username]))
        self.assertTrue(FriendRequest.objects.filter(from_user=self.user1, to_user=self.user2).exists())

    def test_user_detail(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('user_detail', args=[self.user2.username]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user2)
        self.assertFalse(response.context['users_with_request'])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/account/login/?next=/account/')
