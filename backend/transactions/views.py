import csv
from datetime import date
from decimal import Decimal
from django.http import HttpResponse
from django.db.models import Sum, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Transaction
from .serializers import TransactionSerializer, TransactionListSerializer
from .filters import TransactionFilter


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TransactionFilter
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date', '-created_at']

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return TransactionListSerializer
        return TransactionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def report(self, request):
        month_param = request.query_params.get('month')
        
        if month_param:
            try:
                year, month = month_param.split('-')
                year, month = int(year), int(month)
            except (ValueError, AttributeError):
                year, month = date.today().year, date.today().month
        else:
            year, month = date.today().year, date.today().month
        
        queryset = self.get_queryset().filter(
            date__year=year,
            date__month=month
        )
        
        total_income = queryset.filter(
            transaction_type='receita'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        total_expenses = queryset.filter(
            transaction_type='despesa'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        by_category = queryset.filter(
            transaction_type='despesa'
        ).values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        return Response({
            'month': f'{year:04d}-{month:02d}',
            'total_income': str(total_income),
            'total_expenses': str(total_expenses),
            'balance': str(total_income - total_expenses),
            'by_category': [
                {'category': item['category'], 'total': str(item['total'])}
                for item in by_category
            ]
        })

    @action(detail=False, methods=['get'])
    def export(self, request):
        month_param = request.query_params.get('month')
        queryset = self.get_queryset()
        
        if month_param:
            try:
                year, month = month_param.split('-')
                queryset = queryset.filter(
                    date__year=int(year),
                    date__month=int(month)
                )
            except (ValueError, AttributeError):
                pass
        
        queryset = queryset.order_by('-date', '-created_at')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="transacoes_{date.today()}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Data', 'Tipo', 'Categoria', 'Descricao', 'Valor'])
        
        for transaction in queryset:
            writer.writerow([
                transaction.date.strftime('%d/%m/%Y'),
                transaction.get_transaction_type_display(),
                transaction.get_category_display(),
                transaction.description,
                str(transaction.amount)
            ])
        
        return response
