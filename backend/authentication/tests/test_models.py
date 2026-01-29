import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


@pytest.mark.django_db
class TestCustomUserModel:
    
    def test_create_user_with_email_successful(self):
        """Teste: criar usuário com email como identificador"""
        email = 'test@example.com'
        password = 'testpass123'
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name='Test'
        )
        
        assert user.email == email
        assert user.check_password(password)
        assert user.first_name == 'Test'
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    def test_new_user_email_normalized(self):
        """Teste: email do novo usuário é normalizado"""
        email = 'test@EXAMPLE.COM'
        user = User.objects.create_user(
            email=email,
            password='testpass123',
            first_name='Test'
        )
        
        assert user.email == 'test@example.com'

    def test_new_user_without_email_raises_error(self):
        """Teste: criar usuário sem email gera erro"""
        with pytest.raises(ValueError):
            User.objects.create_user(
                email='',
                password='testpass123',
                first_name='Test'
            )

    def test_create_superuser(self):
        """Teste: criar superusuário com permissões corretas"""
        user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123',
            first_name='Admin'
        )
        
        assert user.is_superuser
        assert user.is_staff

    def test_user_email_unique(self):
        """Teste: email deve ser único"""
        User.objects.create_user(
            email='unique@example.com',
            password='testpass123',
            first_name='First'
        )
        
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email='unique@example.com',
                password='testpass456',
                first_name='Second'
            )

    def test_user_str_representation(self):
        """Teste: representação string do usuário é o email"""
        user = User.objects.create_user(
            email='str@example.com',
            password='testpass123',
            first_name='Test'
        )
        
        assert str(user) == 'str@example.com'

    def test_user_first_name_required(self):
        """Teste: primeiro nome é obrigatório via manager"""
        user = User.objects.create_user(
            email='noname@example.com',
            password='testpass123',
            first_name='Required'
        )
        assert user.first_name == 'Required'
