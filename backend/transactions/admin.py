from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'category', 'transaction_type', 'date', 'user')
    list_filter = ('transaction_type', 'category', 'date')
    search_fields = ('description', 'user__email')
    date_hierarchy = 'date'
    ordering = ('-date',)
