from django.urls import path
from app.tests.views import (
    StartTestView,
    SubmitAnswerView,
    FinishTestsView,
)

urlpatterns = [
    path("start/", StartTestView.as_view()),
    path("answer/", SubmitAnswerView.as_view()),
    path("finishh/", FinishTestsView.as_view()),
]
