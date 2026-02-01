from rest_framework.generics import ListAPIView
from django.core.cache import cache

from app.subjects.selectors import subject_list_selector
from app.subjects.serializers import SubjectListSerializer


class SubjectListView(ListAPIView):
    serializer_class = SubjectListSerializer
    pagination_class = None  # Frontend boshqaradi

    def get_queryset(self):
        cache_key = "subjects:list"

        queryset = cache.get(cache_key)
        if not queryset:
            queryset = subject_list_selector()
            cache.set(cache_key, queryset, timeout=60 * 10)  # 10 min

        return queryset
