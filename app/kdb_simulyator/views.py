from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from .models import KDBEntry
from .serializers import KDBSearchSerializer


class KDBSearchPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100


class KDBSearchAPIView(ListAPIView):
    serializer_class = KDBSearchSerializer
    pagination_class = KDBSearchPagination

    def get_queryset(self):
        query = self.request.query_params.get("q", "").strip()

        if not query:
            return KDBEntry.objects.none()

        return (
            KDBEntry.objects
            .filter(
                Q(code__istartswith=query) |
                Q(title__icontains=query)
            )
            .order_by("code")[:50]
        )