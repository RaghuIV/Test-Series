from rest_framework import serializers
from .models import TestSeries, Tag, Exam, Question

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag model"""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']


class TestSeriesSerializer(serializers.ModelSerializer):
    """
    Serializer for the TestSeries model.
    """
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = TagSerializer(many=True, required=False)
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = TestSeries
        fields = [
            'id', 'creator', 'title', 'description', 'price',
            'discount_type', 'discount_value', 'discounted_price', 'discount_start', 'discount_end',
            'is_published', 'created_at', 'updated_at', 'tags'
        ]
        read_only_fields = ['created_at', 'updated_at', 'tags']
    
    def get_discounted_price(self, obj):
        """
        Return the discounted price using model's get_discounted_price method.
        """
        return obj.get_discounted_price()

    # def create(self, validated_data):
    #     test_series = TestSeries.objects.create(**validated_data)
    #     return test_series

    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance

class ExamSerializer(serializers.ModelSerializer):
    """
    Serializer for the Exam model.
    """
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Exam
        fields = [
            'id', 'creator', 'test_series', 'title', 'description',
            'duration_minutes', 'scheduled_at', 'is_live', 'marks',
            'is_published', 'tags', 'negative_marking', 'negative_marks_per_question',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'tags']

    # def create(self, validated_data):
    #     exam = Exam.objects.create(**validated_data)

    #     return exam

    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()

    #     return instance
    
class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Question model without tag support.
    """
    tags = TagSerializer(many=True, required=False)
    
    class Meta:
        model = Question
        fields = [
            "id",
            "exam",
            "text",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_option",
            'tags'
        ]
        read_only_fields = ['tags']
