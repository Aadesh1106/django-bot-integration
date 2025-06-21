from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Public and Protected endpoints
    path('public/', views.public_endpoint, name='public_endpoint'),
    path('protected/', views.protected_endpoint, name='protected_endpoint'),
    
    # Authentication endpoints
    path('register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Post endpoints
    path('posts/', views.PostListCreateView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
]