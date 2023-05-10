from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from .forms import UserRegistrationForm
from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer


@login_required
def dashboard(request):
    return render(
        request,
        'account/dashboard.html',
        {'section': 'dashboard'}
    )


class RegisterUser(View):
    template_name = 'account/register.html'

    def get(self, request):
        context = {
            'user_form': UserRegistrationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()
            username = registration_form.cleaned_data.get('username')
            password = registration_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
        context = {
            'user_form': registration_form
        }
        return render(request, self.template_name, context)


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(
        request,
        'account/user/list.html',
        {'section': 'people', 'users': users}
    )


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    users_with_request = FriendRequest.objects.filter(to_user=user).values_list('from_user', flat=True)
    return render(
        request,
        'account/user/detail.html',
        {'section': 'people', 'user': user, 'users_with_request': users_with_request}
    )


@require_POST
@login_required
def send_friend_request(request, username):
    to_user = User.objects.get(username=username)
    request_to_sender = FriendRequest.objects.filter(from_user=to_user, to_user=request.user).first()
    if request_to_sender:
        request_to_sender.delete()
        request.user.friends.add(to_user)
        to_user.friends.add(request.user)
    else:
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    return redirect('user_detail', username=username)


@require_POST
@login_required
def cancel_friend_request(request, username):
    to_user = User.objects.get(username=username)
    friend_request = FriendRequest.objects.get(from_user=request.user, to_user=to_user)
    friend_request.delete()
    return redirect(request.META.get('HTTP_REFERER', reverse('user_detail', args=[username])))


@require_POST
@login_required
def accept_friend_request(request, from_user):
    from_user = User.objects.get(username=from_user)
    friend_request = FriendRequest.objects.get(from_user=from_user, to_user=request.user)
    friend_request.delete()
    friend_request.from_user.friends.add(friend_request.to_user)
    request.user.friends.add(friend_request.from_user)
    return redirect(request.META.get('HTTP_REFERER', reverse('request_list')))


@require_POST
@login_required
def decline_friend_request(request, from_user):
    from_user = User.objects.get(username=from_user)
    friend_request = FriendRequest.objects.get(from_user=from_user, to_user=request.user)
    friend_request.delete()
    return redirect(request.META.get('HTTP_REFERER', reverse('request_list')))


@require_POST
@login_required
def delete_from_friends(request, username):
    friend = User.objects.get(username=username)
    request.user.friends.remove(friend)
    friend.friends.remove(request.user)
    request.user.save()
    return redirect(request.META.get('HTTP_REFERER', reverse('user_detail', args=[username])))


@login_required
def friend_list(request):
    friends = request.user.friends.all()
    return render(
        request,
        'account/user/list.html',
        {
            'section': 'friends',
            'users': friends
        }
    )


@login_required
def request_list(request):
    sent_requests = FriendRequest.objects.filter(from_user=request.user)
    received_requests = FriendRequest.objects.filter(to_user=request.user)
    return render(
            request,
            'account/user/friend_requests.html',
            {
                'section': 'requests',
                'sent_requests': sent_requests,
                'received_requests': received_requests,
            }
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
