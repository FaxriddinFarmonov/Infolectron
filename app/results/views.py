from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from app.common.permissions import IsAdminUserCustom
from app.results.selectors import admin_subject_analytics_selector
from app.results.serializers import AdminSubjectAnalyticsSerializer



from app.results.selectors import (
    user_test_results_selector,
    user_subject_progress_selector,
)
from app.results.serializers import (
    SubjectProgressSerializer,
    TestHistorySerializer,
)


class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        progress = user_subject_progress_selector(request.user)
        history = user_test_results_selector(request.user)

        return Response({
            "progress": SubjectProgressSerializer(progress, many=True).data,
            "test_history": TestHistorySerializer(history, many=True).data,
        })


class AdminDashboardView(APIView):
    permission_classes = [IsAdminUserCustom]

    def get(self, request):
        analytics = admin_subject_analytics_selector()

        return Response({
            "subjects": AdminSubjectAnalyticsSerializer(
                analytics,
                many=True
            ).data
        })
