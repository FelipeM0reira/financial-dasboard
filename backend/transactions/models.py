from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class Transaction(models.Model):
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
    
    TYPES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='usuário'
    )
    amount = models.DecimalField(
        'valor',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    description = models.CharField('descrição', max_length=255)
    category = models.CharField('categoria', max_length=50, choices=CATEGORIES)
    transaction_type = models.CharField('tipo', max_length=10, choices=TYPES)
    date = models.DateField('data')
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'transação'
        verbose_name_plural = 'transações'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.description} - R$ {self.amount}"
