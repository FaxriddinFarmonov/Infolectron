

from django.urls import path, include

urlpatterns = [
    path("api/auth/", include("app.users.urls")),
    path("api/subjects/", include("app.subjects.urls")),
    path("api/lessons/", include("app.lessons.urls")),
    path("api/tests/", include("app.tests.urls")),
    path("api/results/", include("app.results.urls")),
]
