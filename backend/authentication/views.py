from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from .serializers import (
    RegisterSerializer, 
    CustomTokenObtainPairSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    UserSerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'message': 'Usuário criado com sucesso!'
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            reset_url = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"
            
            send_mail(
                subject='Redefinição de Senha - Budget Tracker',
                message=f'Clique no link para redefinir sua senha: {reset_url}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=f'''
                <html>
                <body>
                    <h2>Redefinição de Senha</h2>
                    <p>Olá {user.first_name},</p>
                    <p>Você solicitou a redefinição de senha da sua conta no Budget Tracker.</p>
                    <p>Clique no botão abaixo para criar uma nova senha:</p>
                    <a href="{reset_url}" style="display: inline-block; padding: 10px 20px; background-color: #3b82f6; color: white; text-decoration: none; border-radius: 5px;">Redefinir Senha</a>
                    <p>Se você não solicitou esta redefinição, ignore este email.</p>
                    <p>Este link expira em 24 horas.</p>
                </body>
                </html>
                '''
            )
        except User.DoesNotExist:
            pass
        
        return Response({
            'message': 'Se o email existir em nossa base, você receberá um link para redefinição de senha.'
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({
                'error': 'Link de redefinição inválido.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        token = serializer.validated_data['token']
        if not default_token_generator.check_token(user, token):
            return Response({
                'error': 'Link de redefinição inválido ou expirado.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Senha redefinida com sucesso!'
        }, status=status.HTTP_200_OK)


class CurrentUserView(generics.RetrieveAPIView):
    """Get current authenticated user information"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
