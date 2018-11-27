from rest_framework import serializers

from backend.companies.models import CompanyStockQuote


class CompanyStockQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyStockQuote
        fields = '__all__'
