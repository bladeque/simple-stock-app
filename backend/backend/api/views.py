import bleach
import requests

from django.core.cache import cache
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from backend.api.serializers import CompanyStockQuoteSerializer
from backend.taskapp.celery import fetch_company_info


class SearchSymbol(APIView):
    """
    A view for searching companies based on their symbol
    """

    def get(self, request, format=None):
        """Returns a list of best matching companies for a given symbol"""

        if 'query' not in request.query_params:
            return (
                Response(
                    'Please provide the `query` parameter',
                    status=status.HTTP_400_BAD_REQUEST,
                )
            )

        symbol = bleach.clean(request.query_params['query'])

        cache_key = f'symbol: {symbol}'

        results = cache.get(cache_key)

        if not results:
            results = requests.get(
                settings.ALPHA_VANTAGE_API_URL,
                params={
                    'function': 'SYMBOL_SEARCH',
                    'keywords': symbol,
                    'apikey': settings.ALPHA_VANTAGE_API_URL,
                }
            )

            try:
                best_matches = results.json()['bestMatches']
            except (ValueError, KeyError):
                return (
                    Response(
                        'Unable to fetch data',
                        status=status.HTTP_404_NOT_FOUND,
                    )
                )

            fetch_company_info.delay(best_matches)

            results = [
                {
                    'symbol': r.get('1. symbol'),
                    'name': r.get('2. name'),
                }
                for r in best_matches
            ]

            cache.set(cache_key, results)

        return Response(results)


class CompanyInfo(ViewSet):
    """
    A view serving company related data
    """

    def retrieve(self, request, pk=None):
        """Retrieve a company info"""
        symbol = pk

        cache_key = f'info_{symbol}'

        company_info = cache.get(cache_key)

        if not company_info:
            return (
                Response('Company not found', status=status.HTTP_404_NOT_FOUND)
            )

        return Response(company_info)

    @action(methods=['post'], detail=True)
    def save_quote(self, request, pk=None):
        # Note: we might in future implement some logic around saving just
        # one quote for a given time period.
        serializer = CompanyStockQuoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('Quote has been saved', status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=True)
    def latest_quote(self, request, pk=None):
        # Note: my assumption is that `the last trading day` means
        # the latest price and volume information.
        symbol = pk

        resp = requests.get(
            settings.ALPHA_VANTAGE_API_URL,
            params={
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': settings.ALPHA_VANTAGE_API_URL,
            }
        )

        try:
            quote = (
                resp.json()
                    .get('Global Quote', {})
            )
        except ValueError:
            return Response(
                'Unable to fetch data',
                status=status.HTTP_404_NOT_FOUND,
            )

        quote = {
            'symbol': symbol,
            'open': quote.get('02. open'),
            'high': quote.get('03. high'),
            'low': quote.get('04. low'),
            'close': quote.get('08. previous close'),
            'price': quote.get('05. price'),
            'volume': quote.get('06. volume'),
        }

        return Response(quote)
