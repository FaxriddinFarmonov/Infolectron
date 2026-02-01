from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include('app.users.urls')),
    path('api/subjects/', include('app.subjects.urls')),
    path('api/lessons/', include('app.lessons.urls')),
    path('api/tests/', include('app.tests.urls')),
    path('api/results/', include('app.results.urls')),
    # path('api/games/', include('app.games.urls')),
    # hali yo‘q bo‘lsa komment qilinadi
]
