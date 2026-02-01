from django.urls import path
from app.subjects.views import SubjectListView

urlpatterns = [
    path("", SubjectListView.as_view()),
]
