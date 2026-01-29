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
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def sample_transactions(user):
    transactions = [
        Transaction.objects.create(
            user=user,
            amount=Decimal('5000.00'),
            description='Salário',
            category='salario',
            transaction_type='receita',
            date=date(2024, 1, 5)
        ),
        Transaction.objects.create(
            user=user,
            amount=Decimal('800.00'),
            description='Supermercado',
            category='alimentacao',
            transaction_type='despesa',
            date=date(2024, 1, 10)
        ),
        Transaction.objects.create(
            user=user,
            amount=Decimal('200.00'),
            description='Restaurante',
            category='alimentacao',
            transaction_type='despesa',
            date=date(2024, 1, 15)
        ),
        Transaction.objects.create(
            user=user,
            amount=Decimal('400.00'),
            description='Uber',
            category='transporte',
            transaction_type='despesa',
            date=date(2024, 1, 20)
        ),
        Transaction.objects.create(
            user=user,
            amount=Decimal('1000.00'),
            description='Aluguel',
            category='moradia',
            transaction_type='despesa',
            date=date(2024, 1, 1)
        ),
    ]
    return transactions


@pytest.mark.django_db
class TestMonthlyReport:
    
    def test_monthly_report_success(self, authenticated_client, sample_transactions):
        """Teste: relatório mensal retorna dados corretos"""
        url = reverse('transactions:transaction-report') + '?month=2024-01'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['month'] == '2024-01'
        assert Decimal(response.data['total_income']) == Decimal('5000.00')
        assert Decimal(response.data['total_expenses']) == Decimal('2400.00')
        assert Decimal(response.data['balance']) == Decimal('2600.00')

    def test_monthly_report_by_category(self, authenticated_client, sample_transactions):
        """Teste: relatório inclui totais por categoria"""
        url = reverse('transactions:transaction-report') + '?month=2024-01'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'by_category' in response.data
        
        categories = {cat['category']: cat['total'] for cat in response.data['by_category']}
        assert Decimal(categories.get('alimentacao', '0')) == Decimal('1000.00')
        assert Decimal(categories.get('transporte', '0')) == Decimal('400.00')
        assert Decimal(categories.get('moradia', '0')) == Decimal('1000.00')

    def test_monthly_report_no_data_returns_zeros(self, authenticated_client, user):
        """Teste: mês sem dados retorna valores zerados"""
        url = reverse('transactions:transaction-report') + '?month=2025-12'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert Decimal(response.data['total_income']) == Decimal('0.00')
        assert Decimal(response.data['total_expenses']) == Decimal('0.00')
        assert Decimal(response.data['balance']) == Decimal('0.00')

    def test_monthly_report_without_month_param(self, authenticated_client, user):
        """Teste: relatório sem parâmetro de mês usa mês atual"""
        Transaction.objects.create(
            user=user,
            amount=Decimal('100.00'),
            description='Teste',
            category='outros',
            transaction_type='despesa',
            date=date.today()
        )
        
        url = reverse('transactions:transaction-report')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        current_month = date.today().strftime('%Y-%m')
        assert response.data['month'] == current_month

    def test_monthly_report_unauthenticated_fails(self, api_client):
        """Teste: relatório sem autenticação retorna 401"""
        url = reverse('transactions:transaction-report') + '?month=2024-01'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestExportCSV:
    
    def test_export_csv_success(self, authenticated_client, sample_transactions):
        """Teste: exportar CSV retorna arquivo"""
        url = reverse('transactions:transaction-export')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'text/csv'
        assert 'attachment' in response['Content-Disposition']

    def test_export_csv_headers(self, authenticated_client, sample_transactions):
        """Teste: CSV contém headers corretos"""
        url = reverse('transactions:transaction-export')
        response = authenticated_client.get(url)
        
        content = response.content.decode('utf-8')
        lines = content.strip().split('\n')
        headers = lines[0]
        
        assert 'Data' in headers
        assert 'Tipo' in headers
        assert 'Categoria' in headers
        assert 'Descricao' in headers or 'Descrição' in headers
        assert 'Valor' in headers

    def test_export_csv_content(self, authenticated_client, sample_transactions):
        """Teste: CSV contém dados das transações"""
        url = reverse('transactions:transaction-export')
        response = authenticated_client.get(url)
        
        content = response.content.decode('utf-8')
        
        assert 'Salário' in content or 'Salario' in content
        assert '5000' in content
        assert 'Supermercado' in content

    def test_export_csv_filter_by_month(self, authenticated_client, sample_transactions):
        """Teste: exportar CSV com filtro de mês"""
        url = reverse('transactions:transaction-export') + '?month=2024-01'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        content = response.content.decode('utf-8')
        lines = content.strip().split('\n')
        
        assert len(lines) == 6

    def test_export_csv_unauthenticated_fails(self, api_client):
        """Teste: exportar CSV sem autenticação retorna 401"""
        url = reverse('transactions:transaction-export')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_export_csv_empty_returns_headers_only(self, authenticated_client, user):
        """Teste: exportar sem transações retorna apenas headers"""
        url = reverse('transactions:transaction-export') + '?month=2099-12'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        content = response.content.decode('utf-8')
        lines = content.strip().split('\n')
        
        assert len(lines) == 1
