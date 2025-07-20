from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    """
    Model representing reusable tags (e.g., difficulty, topic, category) 
    that can be assigned to TestSeries, Exams, or Questions.
    
    Tags can be user-generated and are dynamically assignable.
    """
    name = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        help_text="User who created this tag (optional)."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TestSeries(models.Model):
    """
    Model representing a test series created by a user (e.g., tutor or admin).

    Includes optional discount logic, publication status, and timestamp tracking.
    """
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_series')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    # Discount fields
    discount_type = models.CharField(
        max_length=10,
        choices=[('percent', 'Percentage'), ('fixed', 'Fixed Amount')],
        null=True,
        blank=True,
        help_text="Choose 'percent' or 'fixed'. Leave blank for no discount."
    )
    discount_value = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Discount value depending on type. e.g., 20 for 20% or ₹20"
    )
    discount_start = models.DateTimeField(null=True, blank=True)
    discount_end = models.DateTimeField(null=True, blank=True)

    is_published = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True, related_name='test_series')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_discounted_price(self):
        """
        Calculate and return the discounted price if within discount period.

        :return: Final price after discount if applicable
        :rtype: Decimal
        """
        now = timezone.now()

        if (
            self.discount_type
            and self.discount_value
            and self.discount_start
            and self.discount_end
            and self.discount_start <= now <= self.discount_end
        ):
            if self.discount_type == 'percent':
                discount_amount = (self.discount_value / 100) * self.price
                return max(self.price - discount_amount, 0)
            elif self.discount_type == 'fixed':
                return max(self.price - self.discount_value, 0)
        return self.price

    def __str__(self):
        return self.title


class Exam(models.Model):
    """
    Model representing an individual exam under a test series.

    Supports live scheduling, negative marking, and duration.
    """
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exams')
    test_series = models.ForeignKey(TestSeries, on_delete=models.CASCADE, related_name='exams', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    scheduled_at = models.DateTimeField(null=True, blank=True)
    is_live = models.BooleanField(default=False)
    marks = models.FloatField(default=1.0)

    is_published = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True, related_name='exams')

    negative_marking = models.BooleanField(default=False)
    negative_marks_per_question = models.FloatField(
        default=0.0,
        help_text="Marks deducted per incorrect answer (e.g., 0.25 or 1.0)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        series_title = self.test_series.title if self.test_series else "No Series"
        return f"{self.title} - {series_title}"


class Question(models.Model):
    """
    Model representing a single multiple-choice question in an exam.

    Includes four options and the correct answer.
    """
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    OPTION_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES)
    tags = models.ManyToManyField(Tag, blank=True, related_name='questions')


    def __str__(self):
        return self.text[:50]


class Purchase(models.Model):
    """
    Model to track when a user purchases a test series.

    Ensures a user cannot purchase the same test series more than once.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_series = models.ForeignKey(TestSeries, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'test_series')


class ExamAttempt(models.Model):
    """
    Model representing a user's attempt at an exam.

    Records start/end time and final score.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(default=0.0)


class Answer(models.Model):
    """
    Model representing an answer selected by a user during an exam attempt.

    Stores the selected option and whether it was correct.
    """
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='attempts')
    selected_option = models.CharField(max_length=1, choices=Question.OPTION_CHOICES)
    is_correct = models.BooleanField(default=False)