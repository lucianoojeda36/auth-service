from django.urls import path
from .views import RegisterView, LoginView, RefreshTokenView, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('token/refresh', RefreshTokenView.as_view(), name='token_refresh'),  # Agrega esta línea
] + router.urls
