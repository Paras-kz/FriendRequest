from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, FriendRequestViewSet, UserSearchView, FriendsListView

router = DefaultRouter()
router.register(r'friend-requests', FriendRequestViewSet, basename='friend-request')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('', include(router.urls)),
]
