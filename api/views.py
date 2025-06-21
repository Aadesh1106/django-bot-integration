from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile, Post
from .serializers import UserRegistrationSerializer, UserProfileSerializer, PostSerializer
from .tasks import send_welcome_email
import logging

logger = logging.getLogger(__name__)

# Public endpoint - accessible to everyone
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_endpoint(request):
    """
    Public API endpoint accessible to everyone
    """
    data = {
        'message': 'This is a public endpoint accessible to everyone!',
        'timestamp': '2024-01-01T00:00:00Z',
        'status': 'success',
        'data': {
            'total_users': User.objects.count(),
            'total_posts': Post.objects.count(),
            'api_version': '1.0.0'
        }
    }
    return Response(data, status=status.HTTP_200_OK)

# Protected endpoint - requires authentication
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def protected_endpoint(request):
    """
    Protected API endpoint accessible only to authenticated users
    """
    user_profile = UserProfile.objects.get(user=request.user)
    serializer = UserProfileSerializer(user_profile)
    
    data = {
        'message': f'Hello {request.user.username}! This is a protected endpoint.',
        'user_info': serializer.data,
        'permissions': 'authenticated_user',
        'status': 'success'
    }
    return Response(data, status=status.HTTP_200_OK)

class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        # Send welcome email asynchronously
        send_welcome_email.delay(user.email, user.username)
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'tokens': {
                'token': token.key,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_login(request):
    """
    User login endpoint
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username and password:
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Login successful',
                'tokens': {
                    'token': token.key,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({
            'error': 'Username and password required'
        }, status=status.HTTP_400_BAD_REQUEST)

class PostListCreateView(generics.ListCreateAPIView):
    """
    List all posts or create a new post (authenticated users only)
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post (authenticated users only)
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only modify their own posts
        return Post.objects.filter(author=self.request.user)