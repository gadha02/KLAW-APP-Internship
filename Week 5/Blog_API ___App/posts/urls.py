from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import PostViewSet, RegisterView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('posts/', RegisterView.as_view(), name='posts'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),  # login url to get token
]
