from rest_framework import serializers
from decimal import Decimal
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'id', 'amount', 'description', 'category', 
            'transaction_type', 'date', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_amount(self, value):
        if value <= Decimal('0'):
            raise serializers.ValidationError('O valor deve ser maior que zero.')
        return value

    def validate_category(self, value):
        valid_categories = [choice[0] for choice in Transaction.CATEGORIES]
        if value not in valid_categories:
            raise serializers.ValidationError(f'Categoria inválida. Opções: {", ".join(valid_categories)}')
        return value

    def validate_transaction_type(self, value):
        valid_types = [choice[0] for choice in Transaction.TYPES]
        if value not in valid_types:
            raise serializers.ValidationError(f'Tipo inválido. Opções: {", ".join(valid_types)}')
        return value


class TransactionListSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)

    class Meta:
        model = Transaction
        fields = (
            'id', 'amount', 'description', 'category', 'category_display',
            'transaction_type', 'type_display', 'date', 'created_at'
        )
