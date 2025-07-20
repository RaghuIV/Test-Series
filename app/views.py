from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import TestSeries, Tag, Exam, Question
from .serializers import TestSeriesSerializer, TagSerializer, ExamSerializer, QuestionSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Tags'])
class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tags.
    - Only authenticated users can create/update/delete.
    - Tags are reusable across TestSeries, Exams, Questions.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Set created_by to the current user
        serializer.save(created_by=self.request.user)

@extend_schema(tags=['TestSeries'])
class TestSeriesViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing TestSeries instances.
    
    Supports list, retrieve, create, update, and delete operations.
    """
    queryset = TestSeries.objects.all()
    serializer_class = TestSeriesSerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema(tags=['Exams'])
class ExamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Exam instances.

    Supports list, retrieve, create, update, delete.
    """
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema(tags=['Question'])
class QuestionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Question instances.

    Provides list, retrieve, create, update, and delete actions.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
