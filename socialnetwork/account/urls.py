from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register', views.RegisterUser.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('users/', views.user_list, name='user_list'),
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('users/<username>/delete-from-friends/', views.delete_from_friends, name='delete_from_friends'),
    path('friends/', views.friend_list, name='friend_list'),
    path('requests/', views.request_list, name='request_list'),
    path('requests/accept-friend-request/<from_user>/', views.accept_friend_request, name='accept_friend_request'),
    path('requests/decline-friend-request/<from_user>/', views.decline_friend_request, name='decline_friend_request'),
    path('requests/send-friend-request/<username>/', views.send_friend_request, name='send_friend_request'),
    path('requests/cancel-friend-request/<username>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('', views.dashboard, name='dashboard'),
]
