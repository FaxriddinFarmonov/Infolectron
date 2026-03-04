from django.urls import path

from app.kdb_simulyator.views import KDBSearchAPIView

urlpatterns = [
    path("search/", KDBSearchAPIView.as_view(), name="kdb-search"),
]