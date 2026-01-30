# Generated migration for RecurringTransaction model

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
import decimal
from datetime import date


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecurringTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='descrição')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(decimal.Decimal('0.01'))], verbose_name='valor')),
                ('category', models.CharField(choices=[('alimentacao', 'Alimentação'), ('transporte', 'Transporte'), ('moradia', 'Moradia'), ('saude', 'Saúde'), ('lazer', 'Lazer'), ('educacao', 'Educação'), ('salario', 'Salário'), ('investimentos', 'Investimentos'), ('outros', 'Outros')], max_length=50, verbose_name='categoria')),
                ('transaction_type', models.CharField(choices=[('receita', 'Receita'), ('despesa', 'Despesa')], max_length=10, verbose_name='tipo')),
                ('frequency', models.CharField(choices=[('daily', 'Diário'), ('weekly', 'Semanal'), ('biweekly', 'Quinzenal'), ('monthly', 'Mensal'), ('quarterly', 'Trimestral'), ('yearly', 'Anual')], max_length=20, verbose_name='frequência')),
                ('start_date', models.DateField(default=date.today, verbose_name='data de início')),
                ('next_execution_date', models.DateField(verbose_name='próxima execução')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='data de término')),
                ('active', models.BooleanField(default=True, verbose_name='ativa')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recurring_transactions', to='authentication.customuser', verbose_name='usuário')),
            ],
            options={
                'verbose_name': 'transação recorrente',
                'verbose_name_plural': 'transações recorrentes',
            },
        ),
    ]
