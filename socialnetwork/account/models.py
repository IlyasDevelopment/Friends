from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):

    friends = models.ManyToManyField("User", blank=True)

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'username': self.username})


class FriendRequest(models.Model):

    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['from_user', 'to_user'], name='friend_request_pk')
        ]
