import pytest
from decimal import Decimal
from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from transactions.models import Transaction

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email='testuser@example.com',
        password='TestPass123!',
        first_name='Test'
    )


@pytest.fixture
def other_user():
    return User.objects.create_user(
        email='other@example.com',
        password='OtherPass123!',
        first_name='Other'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def valid_transaction_data():
    return {
        'amount': '150.50',
        'description': 'Supermercado',
        'category': 'alimentacao',
        'transaction_type': 'despesa',
        'date': str(date.today())
    }


@pytest.fixture
def user_transaction(user):
    return Transaction.objects.create(
        user=user,
        amount=Decimal('100.00'),
        description='Transação do usuário',
        category='outros',
        transaction_type='despesa',
        date=date.today()
    )


@pytest.mark.django_db
class TestCreateTransaction:
    
    def test_create_transaction_authenticated_success(self, authenticated_client, valid_transaction_data):
        """Teste: criar transação autenticado retorna 201"""
        url = reverse('transactions:transaction-list')
        response = authenticated_client.post(url, valid_transaction_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['description'] == valid_transaction_data['description']
        assert Decimal(response.data['amount']) == Decimal(valid_transaction_data['amount'])

    def test_create_transaction_unauthenticated_fails(self, api_client, valid_transaction_data):
        """Teste: criar transação sem autenticação retorna 401"""
        url = reverse('transactions:transaction-list')
        response = api_client.post(url, valid_transaction_data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_transaction_negative_amount_fails(self, authenticated_client, valid_transaction_data):
        """Teste: criar transação com valor negativo retorna 400"""
        valid_transaction_data['amount'] = '-100.00'
        url = reverse('transactions:transaction-list')
        response = authenticated_client.post(url, valid_transaction_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_transaction_zero_amount_fails(self, authenticated_client, valid_transaction_data):
        """Teste: criar transação com valor zero retorna 400"""
        valid_transaction_data['amount'] = '0.00'
        url = reverse('transactions:transaction-list')
        response = authenticated_client.post(url, valid_transaction_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_transaction_invalid_category_fails(self, authenticated_client, valid_transaction_data):
        """Teste: criar transação com categoria inválida retorna 400"""
        valid_transaction_data['category'] = 'categoria_invalida'
        url = reverse('transactions:transaction-list')
        response = authenticated_client.post(url, valid_transaction_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_transaction_missing_fields_fails(self, authenticated_client):
        """Teste: criar transação sem campos obrigatórios retorna 400"""
        url = reverse('transactions:transaction-list')
        response = authenticated_client.post(url, {}, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestListTransactions:
    
    def test_list_transactions_authenticated(self, authenticated_client, user):
        """Teste: listar transações retorna apenas do usuário logado"""
        Transaction.objects.create(
            user=user,
            amount=Decimal('100.00'),
            description='Minha transação',
            category='outros',
            transaction_type='despesa',
            date=date.today()
        )
        
        url = reverse('transactions:transaction-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['description'] == 'Minha transação'

    def test_list_transactions_not_show_others(self, authenticated_client, user, other_user):
        """Teste: não mostra transações de outros usuários"""
        Transaction.objects.create(
            user=user,
            amount=Decimal('100.00'),
            description='Minha',
            category='outros',
            transaction_type='despesa',
            date=date.today()
        )
        Transaction.objects.create(
            user=other_user,
            amount=Decimal('200.00'),
            description='Do outro',
            category='outros',
            transaction_type='despesa',
            date=date.today()
        )
        
        url = reverse('transactions:transaction-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['description'] == 'Minha'

    def test_list_transactions_filter_by_month(self, authenticated_client, user):
        """Teste: filtrar por mês"""
        Transaction.objects.create(
            user=user,
            amount=Decimal('100.00'),
            description='Janeiro',
            category='outros',
            transaction_type='despesa',
            date=date(2024, 1, 15)
        )
        Transaction.objects.create(
            user=user,
            amount=Decimal('200.00'),
            description='Fevereiro',
            category='outros',
            transaction_type='despesa',
            date=date(2024, 2, 15)
        )
        
        url = reverse('transactions:transaction-list') + '?month=2024-01'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['description'] == 'Janeiro'

    def test_list_transactions_filter_by_category(self, authenticated_client, user):
        """Teste: filtrar por categoria"""
        Transaction.objects.create(
            user=user,
            amount=Decimal('100.00'),
            description='Almoço',
            category='alimentacao',
            transaction_type='despesa',
            date=date.today()
        )
        Transaction.objects.create(
            user=user,
            amount=Decimal('200.00'),
            description='Uber',
            category='transporte',
            transaction_type='despesa',
            date=date.today()
        )
        
        url = reverse('transactions:transaction-list') + '?category=alimentacao'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['description'] == 'Almoço'

    def test_list_transactions_filter_by_type(self, authenticated_client, user):
        """Teste: filtrar por tipo"""
        Transaction.objects.create(
            user=user,
            amount=Decimal('5000.00'),
            description='Salário',
            category='salario',
            transaction_type='receita',
            date=date.today()
        )
        Transaction.objects.create(
            user=user,
            amount=Decimal('100.00'),
            description='Almoço',
            category='alimentacao',
            transaction_type='despesa',
            date=date.today()
        )
        
        url = reverse('transactions:transaction-list') + '?transaction_type=receita'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['description'] == 'Salário'

    def test_list_transactions_pagination(self, authenticated_client, user):
        """Teste: paginação funciona corretamente"""
        for i in range(25):
            Transaction.objects.create(
                user=user,
                amount=Decimal('10.00'),
                description=f'Transação {i}',
                category='outros',
                transaction_type='despesa',
                date=date.today()
            )
        
        url = reverse('transactions:transaction-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 20
        assert response.data['count'] == 25
        assert response.data['next'] is not None


@pytest.mark.django_db
class TestUpdateTransaction:
    
    def test_update_own_transaction_success(self, authenticated_client, user_transaction):
        """Teste: atualizar própria transação retorna 200"""
        url = reverse('transactions:transaction-detail', args=[user_transaction.id])
        response = authenticated_client.put(url, {
            'amount': '200.00',
            'description': 'Atualizada',
            'category': 'transporte',
            'transaction_type': 'despesa',
            'date': str(date.today())
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['description'] == 'Atualizada'
        assert Decimal(response.data['amount']) == Decimal('200.00')

    def test_update_other_user_transaction_fails(self, authenticated_client, other_user):
        """Teste: atualizar transação de outro usuário retorna 404"""
        other_transaction = Transaction.objects.create(
            user=other_user,
            amount=Decimal('100.00'),
            description='Do outro',
            category='outros',
            transaction_type='despesa',
            date=date.today()
        )
        
        url = reverse('transactions:transaction-detail', args=[other_transaction.id])
        response = authenticated_client.put(url, {
            'amount': '200.00',
            'description': 'Tentativa',
            'category': 'outros',
            'transaction_type': 'despesa',
            'date': str(date.today())
        }, format='json')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_partial_update_transaction_success(self, authenticated_client, user_transaction):
        """Teste: atualização parcial retorna 200"""
        url = reverse('transactions:transaction-detail', args=[user_transaction.id])
        response = authenticated_client.patch(url, {
            'description': 'Parcialmente atualizada'
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['description'] == 'Parcialmente atualizada'


@pytest.mark.django_db
class TestDeleteTransaction:
    
    def test_delete_own_transaction_success(self, authenticated_client, user_transaction):
        """Teste: deletar própria transação retorna 204"""
        url = reverse('transactions:transaction-detail', args=[user_transaction.id])
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Transaction.objects.filter(id=user_transaction.id).exists()

    def test_delete_other_user_transaction_fails(self, authenticated_client, other_user):
        """Teste: deletar transação de outro usuário retorna 404"""
        other_transaction = Transaction.objects.create(
            user=other_user,
            amount=Decimal('100.00'),
            description='Do outro',
            category='outros',
            transaction_type='despesa',
            date=date.today()
        )
        
        url = reverse('transactions:transaction-detail', args=[other_transaction.id])
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert Transaction.objects.filter(id=other_transaction.id).exists()
