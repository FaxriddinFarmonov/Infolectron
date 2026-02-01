from django.urls import path
from app.results.views import StudentDashboardView
from app.results.views import AdminDashboardView


urlpatterns = [
    path("dashboard/", StudentDashboardView.as_view()),
    path("admin/dashboard/", AdminDashboardView.as_view()),
]
