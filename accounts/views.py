from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import UserSerializer


# Create your views here.

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        
        else:
            return Response({"error_message": "Sorry, we could't fine your account with this email and password."}, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):
    def post(self, request, format=None):
        data = request.data
        full_name = data.get('full_name')
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return Response({'error': 'Name, username, password, and email are required.'}, status=status.HTTP_400_BAD_REQUEST)
        if len(password)<8:
            return Response({'error': 'Password must be at least 8 characters.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(full_name=full_name,username=username, password=password, email=email)
            refresh = RefreshToken.for_user(user)
            return Response({
                'message':'Account created successfully!',
                'access_token': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""Management self account"""
class FollowUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        following = get_object_or_404(User, username=username)
        follower = request.user
        follow = Follow.objects.filter(follower=follower, following=following)
        if follower == following:
            message = f"You can't follow yourself."
        elif follow.exists():
            follow.delete()
            message = f"You have unfollowed {following.username}."
        else:
            Follow.objects.create(follower=follower, following=following)
            message = f"You have followed {following.username}."
        return Response({"message": message}, status=status.HTTP_200_OK)

class EditProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            errors = {}
            for field, messages in serializer.errors.items():
                # Use the field name as the key and the first error message as the value
                errors["message"] = messages[0]

            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if old_password is None or new_password is None:
            return Response({"error": "Both old password and new password are required."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({"error": "Your old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

""" Get more detail or list view about self account """
class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, context={'request':request})
        return Response({
            'success':True,
            'user':serializer.data
        })
    
class UserProfileDetailAPIView(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user, context={'request':request})
        return Response({
            'success':True,
            'user':serializer.data
        })
    
class FollowingUserAPIListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_users = Follow.objects.filter(follower=self.request.user).values_list('following', flat=True)
        users = User.objects.filter(id__in=following_users)

        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response({
            'success':True,
            'followingUsers':serializer.data
        })

class FollowerUserAPIListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        follower_users = Follow.objects.filter(following=self.request.user).values_list('follower', flat=True)
        users = User.objects.filter(id__in=follower_users)
        serializer = UserSerializer(users, many=True, context={'request':request})
        return Response({
            'success':True,
            'followerUsers':serializer.data
        })