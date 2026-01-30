from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from datetime import date


class RecurringTransaction(models.Model):
    """Model for recurring/fixed transactions"""
    
    FREQUENCY_CHOICES = [
        ('daily', 'Diário'),
        ('weekly', 'Semanal'),
        ('biweekly', 'Quinzenal'),
        ('monthly', 'Mensal'),
        ('quarterly', 'Trimestral'),
        ('yearly', 'Anual'),
    ]
    
    TYPES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]
    
    CATEGORIES = [
        ('alimentacao', 'Alimentação'),
        ('transporte', 'Transporte'),
        ('moradia', 'Moradia'),
        ('saude', 'Saúde'),
        ('lazer', 'Lazer'),
        ('educacao', 'Educação'),
        ('salario', 'Salário'),
        ('investimentos', 'Investimentos'),
        ('outros', 'Outros'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recurring_transactions',
        verbose_name='usuário'
    )
    description = models.CharField('descrição', max_length=255)
    amount = models.DecimalField(
        'valor',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    category = models.CharField('categoria', max_length=50, choices=CATEGORIES)
    transaction_type = models.CharField('tipo', max_length=10, choices=TYPES)
    frequency = models.CharField('frequência', max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField('data de início', default=date.today)
    next_execution_date = models.DateField('próxima execução')
    end_date = models.DateField('data de término', null=True, blank=True)
    active = models.BooleanField('ativa', default=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'transação recorrente'
        verbose_name_plural = 'transações recorrentes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.description} - {self.get_frequency_display()} - R$ {self.amount}"

    def get_next_execution_date(self):
        """Calculate next execution date based on frequency"""
        frequency_mapping = {
            'daily': relativedelta(days=1),
            'weekly': relativedelta(weeks=1),
            'biweekly': relativedelta(weeks=2),
            'monthly': relativedelta(months=1),
            'quarterly': relativedelta(months=3),
            'yearly': relativedelta(years=1),
        }
        
        delta = frequency_mapping.get(self.frequency, relativedelta(months=1))
        return self.next_execution_date + delta

    def should_execute(self):
        """Check if transaction should be executed today"""
        today = date.today()
        
        # Check if active and due date has passed
        if not self.active or self.next_execution_date > today:
            return False
        
        # Check if end_date has passed
        if self.end_date and today > self.end_date:
            self.active = False
            self.save()
            return False
        
        return True
