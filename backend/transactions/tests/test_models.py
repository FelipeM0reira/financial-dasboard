import pytest
from decimal import Decimal
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from transactions.models import Transaction

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        email='testuser@example.com',
        password='TestPass123!',
        first_name='Test'
    )


@pytest.mark.django_db
class TestTransactionModel:
    
    def test_create_transaction_successful(self, user):
        """Teste: criar transação com todos os campos"""
        transaction = Transaction.objects.create(
            user=user,
            amount=Decimal('150.50'),
            description='Supermercado',
            category='alimentacao',
            transaction_type='despesa',
            date=date.today()
        )
        
        assert transaction.id is not None
        assert transaction.user == user
        assert transaction.amount == Decimal('150.50')
        assert transaction.description == 'Supermercado'
        assert transaction.category == 'alimentacao'
        assert transaction.transaction_type == 'despesa'

    def test_transaction_decimal_precision(self, user):
        """Teste: valor com precisão de 2 casas decimais"""
        transaction = Transaction.objects.create(
            user=user,
            amount=Decimal('1234.56'),
            description='Teste precisão',
            category='outros',
            transaction_type='despesa',
            date=date.today()
        )
        
        assert transaction.amount == Decimal('1234.56')

    def test_transaction_positive_amount(self, user):
        """Teste: valor deve ser positivo (validado no serializer)"""
        transaction = Transaction.objects.create(
            user=user,
            amount=Decimal('0.01'),
            description='Valor mínimo',
            category='outros',
            transaction_type='despesa',
            date=date.today()
        )
        
        assert transaction.amount == Decimal('0.01')

    def test_transaction_category_choices(self, user):
        """Teste: categoria deve estar nas opções válidas"""
        valid_categories = ['alimentacao', 'transporte', 'moradia', 'saude', 
                          'lazer', 'educacao', 'salario', 'investimentos', 'outros']
        
        for category in valid_categories:
            transaction = Transaction.objects.create(
                user=user,
                amount=Decimal('100.00'),
                description=f'Teste {category}',
                category=category,
                transaction_type='despesa',
                date=date.today()
            )
            assert transaction.category == category

    def test_transaction_type_choices(self, user):
        """Teste: tipo deve ser receita ou despesa"""
        receita = Transaction.objects.create(
            user=user,
            amount=Decimal('5000.00'),
            description='Salário',
            category='salario',
            transaction_type='receita',
            date=date.today()
        )
        
        despesa = Transaction.objects.create(
            user=user,
            amount=Decimal('100.00'),
            description='Almoço',
            category='alimentacao',
            transaction_type='despesa',
            date=date.today()
        )
        
        assert receita.transaction_type == 'receita'
        assert despesa.transaction_type == 'despesa'

    def test_transaction_user_relationship(self, user):
        """Teste: transação está relacionada ao usuário"""
        transaction = Transaction.objects.create(
            user=user,
            amount=Decimal('100.00'),
            description='Teste relação',
            category='outros',
            transaction_type='despesa',
            date=date.today()
        )
        
        assert transaction in user.transactions.all()

    def test_transaction_str_representation(self, user):
        """Teste: representação string da transação"""
        transaction = Transaction.objects.create(
            user=user,
            amount=Decimal('100.00'),
            description='Teste str',
            category='outros',
            transaction_type='despesa',
            date=date.today()
        )
        
        assert 'Despesa' in str(transaction)
        assert 'Teste str' in str(transaction)
        assert '100.00' in str(transaction)

    def test_transaction_ordering(self, user):
        """Teste: transações ordenadas por data decrescente"""
        t1 = Transaction.objects.create(
            user=user,
            amount=Decimal('100.00'),
            description='Antiga',
            category='outros',
            transaction_type='despesa',
            date=date(2024, 1, 1)
        )
        
        t2 = Transaction.objects.create(
            user=user,
            amount=Decimal('200.00'),
            description='Recente',
            category='outros',
            transaction_type='despesa',
            date=date(2024, 1, 15)
        )
        
        transactions = Transaction.objects.all()
        assert transactions[0] == t2
        assert transactions[1] == t1

    def test_transaction_created_at_auto(self, user):
        """Teste: campo created_at é preenchido automaticamente"""
        transaction = Transaction.objects.create(
            user=user,
            amount=Decimal('100.00'),
            description='Teste auto',
            category='outros',
            transaction_type='despesa',
            date=date.today()
        )
        
        assert transaction.created_at is not None
