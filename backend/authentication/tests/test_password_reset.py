import pytest
from django.urls import reverse
from django.core import mail
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email='reset@example.com',
        password='OldPass123!',
        first_name='Reset'
    )


@pytest.mark.django_db
class TestPasswordResetRequest:
    
    def test_password_reset_request_valid_email(self, api_client, user):
        """Teste: solicitação de reset com email válido retorna 200"""
        url = reverse('auth:password_reset_request')
        response = api_client.post(url, {'email': user.email}, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data

    def test_password_reset_request_sends_email(self, api_client, user):
        """Teste: solicitação de reset envia email"""
        url = reverse('auth:password_reset_request')
        api_client.post(url, {'email': user.email}, format='json')
        
        assert len(mail.outbox) == 1
        assert user.email in mail.outbox[0].to

    def test_password_reset_request_nonexistent_email_returns_200(self, api_client):
        """Teste: email inexistente retorna 200 por segurança"""
        url = reverse('auth:password_reset_request')
        response = api_client.post(url, {'email': 'nonexistent@example.com'}, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(mail.outbox) == 0

    def test_password_reset_request_invalid_email_format(self, api_client):
        """Teste: email inválido retorna 400"""
        url = reverse('auth:password_reset_request')
        response = api_client.post(url, {'email': 'invalid-email'}, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPasswordResetConfirm:
    
    def test_password_reset_confirm_valid_token(self, api_client, user):
        """Teste: confirmação de reset com token válido retorna 200"""
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        url = reverse('auth:password_reset_confirm')
        response = api_client.post(url, {
            'uid': uid,
            'token': token,
            'new_password': 'NewSecurePass123!',
            'new_password_confirm': 'NewSecurePass123!'
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        user.refresh_from_db()
        assert user.check_password('NewSecurePass123!')

    def test_password_reset_confirm_invalid_token(self, api_client, user):
        """Teste: token inválido retorna 400"""
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        url = reverse('auth:password_reset_confirm')
        response = api_client.post(url, {
            'uid': uid,
            'token': 'invalid-token',
            'new_password': 'NewSecurePass123!',
            'new_password_confirm': 'NewSecurePass123!'
        }, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_reset_confirm_invalid_uid(self, api_client):
        """Teste: UID inválido retorna 400"""
        url = reverse('auth:password_reset_confirm')
        response = api_client.post(url, {
            'uid': 'invalid-uid',
            'token': 'some-token',
            'new_password': 'NewSecurePass123!',
            'new_password_confirm': 'NewSecurePass123!'
        }, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_reset_confirm_password_mismatch(self, api_client, user):
        """Teste: senhas diferentes retorna 400"""
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        url = reverse('auth:password_reset_confirm')
        response = api_client.post(url, {
            'uid': uid,
            'token': token,
            'new_password': 'NewSecurePass123!',
            'new_password_confirm': 'DifferentPass123!'
        }, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_reset_confirm_weak_password(self, api_client, user):
        """Teste: senha fraca retorna 400"""
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        url = reverse('auth:password_reset_confirm')
        response = api_client.post(url, {
            'uid': uid,
            'token': token,
            'new_password': '123',
            'new_password_confirm': '123'
        }, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
