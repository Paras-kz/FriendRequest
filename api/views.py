from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser, FriendRequest
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .serializers import LoginSerializer, FriendRequestSerializer, UserSerializer
from rest_framework.exceptions import Throttled
from rest_framework.throttling import UserRateThrottle

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
     #when serialixer obj is called, in serializer.py file create fn is redifned
    #otherewise we could custom define the post method with APIview, read variables values
    #from requests.data.get('email) then..
    #user = CustomUser.objects.create_user(email=email, username=username, password=password)
    # Serialize the user data
    #user_serializer = UserSerializer(user)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'].lower()
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPagination(PageNumberPagination):
    page_size = 10

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = UserPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '').lower()
        if '@' in query:
            return CustomUser.objects.filter(email__iexact=query)
        return CustomUser.objects.filter(username__icontains=query)
# class UserSearchView(generics.ListAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['email', 'username']
#     pagination_class = PageNumberPagination

#     class PageNumberPagination(PageNumberPagination):
#         page_size = 10

class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user, status='pending')

    def perform_create(self, serializer):
        from_user = self.request.user
        to_user_id = self.request.data.get('to_user')
        to_user = CustomUser.objects.get(id=to_user_id)
        # Apply UserRateThrottle for 'friend_request' scope
        throttle = UserRateThrottle()
        throttle.scope = 'send_req'
        if not throttle.allow_request(self.request, self):
            raise Throttled(detail="can't send more than 3 req. in a minute")
        # Throttle friend requests (no more than 3 within a minute)
        # one_minute_ago = timezone.now() - timedelta(minutes=1)
        # recent_requests = FriendRequest.objects.filter(from_user=from_user, timestamp__gte=one_minute_ago)
        # if recent_requests.count() >= 3:
        #     raise serializers.ValidationError('Too many friend requests sent in a short time')

        serializer.save(from_user=from_user, to_user=to_user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()   # Retrieves the FriendRequest object based on the URL pk
        if instance.to_user != request.user:
            return Response({'detail': 'Not authorized to update this request'}, status=status.HTTP_403_FORBIDDEN)
        
        status = request.data.get('status')
        if status in ['accepted', 'rejected']:
            instance.status = status
            instance.save()
            return Response({'status': instance.status}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

class FriendsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        friends = CustomUser.objects.filter(
            id__in=FriendRequest.objects.filter(
                (Q(from_user=user) | Q(to_user=user)),
                status='accepted'
            ).values_list('from_user', 'to_user')
        ).exclude(id=user.id)
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)


# class FriendsListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user

#         # Get the IDs of users who are friends with the current user
#         friend_requests = FriendRequest.objects.filter(
#             (Q(from_user=user) | Q(to_user=user)),
#             status='accepted'
#         )

#         friend_ids = set()
#         for fr in friend_requests:
#             if fr.from_user != user:
#                 friend_ids.add(fr.from_user.id)
#             if fr.to_user != user:
#                 friend_ids.add(fr.to_user.id)

#         # Retrieve the CustomUser instances for these IDs
#         friends = CustomUser.objects.filter(id__in=friend_ids)

#         # Serialize the friends list
#         serializer = UserSerializer(friends, many=True)
#         return Response(serializer.data)

