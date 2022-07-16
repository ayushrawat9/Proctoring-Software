from django.db import models
from django_base64field.fields import Base64Field
from django.utils import timezone


class ProctoringLog(models.Model):
    student_id = models.CharField(max_length=100)
    test_id = models.CharField(max_length=100)
    flag = models.CharField(max_length=100)
    image = models.ImageField(upload_to="saved_log_images/")
    timestamp = models.TimeField(default=timezone.now)


class TestResult(models.Model):
    student_id = models.CharField(max_length=100)
    test_id = models.CharField(max_length=100)
    marks = models.IntegerField()

    class Meta:
        unique_together = ('test_id', 'student_id',)

# Create your models here.
