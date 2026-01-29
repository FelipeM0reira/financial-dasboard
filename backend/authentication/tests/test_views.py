import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def valid_user_data():
    return {
        'email': 'newuser@example.com',
        'password': 'SecurePass123!',
        'password_confirm': 'SecurePass123!',
        'first_name': 'John',
        'last_name': 'Doe'
    }


@pytest.mark.django_db
class TestRegisterView:
    
    def test_register_user_success(self, api_client, valid_user_data):
        """Teste: registro com dados válidos retorna 201"""
        url = reverse('auth:register')
        response = api_client.post(url, valid_user_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'email' in response.data
        assert response.data['email'] == valid_user_data['email']
        assert 'password' not in response.data
        assert User.objects.filter(email=valid_user_data['email']).exists()

    def test_register_user_with_existing_email_fails(self, api_client, valid_user_data):
        """Teste: registro com email duplicado retorna 400"""
        User.objects.create_user(
            email=valid_user_data['email'],
            password='existingpass123',
            first_name='Existing'
        )
        
        url = reverse('auth:register')
        response = api_client.post(url, valid_user_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_register_user_weak_password_fails(self, api_client, valid_user_data):
        """Teste: registro com senha fraca retorna 400"""
        valid_user_data['password'] = '123'
        valid_user_data['password_confirm'] = '123'
        
        url = reverse('auth:register')
        response = api_client.post(url, valid_user_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_user_password_mismatch_fails(self, api_client, valid_user_data):
        """Teste: registro com senhas diferentes retorna 400"""
        valid_user_data['password_confirm'] = 'DifferentPass123!'
        
        url = reverse('auth:register')
        response = api_client.post(url, valid_user_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data or 'password_confirm' in response.data

    def test_register_user_missing_email_fails(self, api_client, valid_user_data):
        """Teste: registro sem email retorna 400"""
        del valid_user_data['email']
        
        url = reverse('auth:register')
        response = api_client.post(url, valid_user_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_register_user_missing_first_name_fails(self, api_client, valid_user_data):
        """Teste: registro sem primeiro nome retorna 400"""
        del valid_user_data['first_name']
        
        url = reverse('auth:register')
        response = api_client.post(url, valid_user_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'first_name' in response.data

    def test_register_user_invalid_email_format_fails(self, api_client, valid_user_data):
        """Teste: registro com email inválido retorna 400"""
        valid_user_data['email'] = 'invalid-email'
        
        url = reverse('auth:register')
        response = api_client.post(url, valid_user_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data


@pytest.mark.django_db
class TestLoginView:
    
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            email='testuser@example.com',
            password='TestPass123!',
            first_name='Test'
        )

    def test_login_success(self, api_client, user):
        """Teste: login com credenciais válidas retorna 200 + tokens"""
        url = reverse('auth:login')
        data = {
            'email': 'testuser@example.com',
            'password': 'TestPass123!'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_invalid_credentials_fails(self, api_client, user):
        """Teste: login com credenciais inválidas retorna 401"""
        url = reverse('auth:login')
        data = {
            'email': 'testuser@example.com',
            'password': 'WrongPassword123!'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user_fails(self, api_client):
        """Teste: login com usuário inexistente retorna 401"""
        url = reverse('auth:login')
        data = {
            'email': 'nonexistent@example.com',
            'password': 'SomePass123!'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestTokenRefresh:
    
    @pytest.fixture
    def user_with_tokens(self, api_client):
        user = User.objects.create_user(
            email='refresh@example.com',
            password='RefreshPass123!',
            first_name='Refresh'
        )
        login_url = reverse('auth:login')
        response = api_client.post(login_url, {
            'email': 'refresh@example.com',
            'password': 'RefreshPass123!'
        }, format='json')
        return response.data

    def test_token_refresh_success(self, api_client, user_with_tokens):
        """Teste: refresh token válido retorna novo access token"""
        url = reverse('auth:token_refresh')
        response = api_client.post(url, {
            'refresh': user_with_tokens['refresh']
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_token_refresh_invalid_fails(self, api_client):
        """Teste: refresh token inválido retorna 401"""
        url = reverse('auth:token_refresh')
        response = api_client.post(url, {
            'refresh': 'invalid-token'
        }, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
