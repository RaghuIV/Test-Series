# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, TestSeriesViewSet, ExamViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'test-series', TestSeriesViewSet, basename='testseries')
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r"questions", QuestionViewSet, basename="question")

urlpatterns = [
    path('', include(router.urls)),
]
