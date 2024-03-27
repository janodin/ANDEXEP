from django.db import models


class StressLevelRecord(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=255)
    bmi_category = models.CharField(max_length=255)
    phq1 = models.IntegerField()
    phq2 = models.IntegerField()
    phq3 = models.IntegerField()
    phq4 = models.IntegerField()
    phq5 = models.IntegerField()
    phq6 = models.IntegerField()
    phq7 = models.IntegerField()
    phq8 = models.IntegerField()
    phq9 = models.IntegerField()
    phq_score_total = models.IntegerField()
    is_suicide = models.CharField(max_length=255)
    stress_level = models.CharField(max_length=255)
    recommendations = models.TextField()
