import logging
import jwt
import datetime
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model, authenticate
from .serializers import UserSerializer

User = get_user_model()

# Set up logger
logger = logging.getLogger(__name__)

# Helper function to generate a JWT token
def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),  # Token expiration
        'iat': datetime.datetime.utcnow(),  # Token issued at
    }
    
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')

    return token

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user.pk:
                access_token = generate_jwt_token(user)

                logger.info(f"New user registered: {user.email}")

                return Response({
                    'access': access_token,
                    'user': serializer.data
                }, status=status.HTTP_201_CREATED)
        logger.error(f"Error during registration: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        
        if user is not None:
            access_token = generate_jwt_token(user)
            logger.info(f"Authenticated user: {user.email}")
            return Response({'access': access_token})
        
        logger.warning(f"Failed login attempt for: {email}")
        return Response({"error": "Invalid credentials"}, status=400)

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if refresh_token is None:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode the refresh token
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])

            # Generate a new access token
            user_id = payload.get('user_id')
            user = User.objects.get(id=user_id)

            new_access_token = generate_jwt_token(user)

            return Response({"access": new_access_token}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            logger.error("The refresh token has expired")
            return Response({"error": "Refresh token expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError as e:
            logger.error(f"Error refreshing token: {str(e)}")
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
