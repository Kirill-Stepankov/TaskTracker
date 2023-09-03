from django.db import models

class Task(models.Model):
    class StatusChoices(models.TextChoices):
        TO_DO = 'TD', 'TO DO'
        IN_PROGRESS = 'IP', 'IN PROGRESS'
        DONE = 'DN', 'DONE'

    class PriorityChoices(models.TextChoices):
        HIGH = 'HG', 'High'
        MEDIUM = 'MD', 'Medium'
        LOW = 'LW', 'Low'

    class CategoryChoices(models.TextChoices):
        WORK = 'WK', 'Work'
        HOME = 'HM', 'Home'
        LEARNING = 'LN', 'Learning'
        OTHER = 'TH', 'Other'

    description = models.TextField()
    status = models.CharField(max_length=2, choices=StatusChoices.choices, default=StatusChoices.TO_DO)
    priority = models.CharField(max_length=2, choices=PriorityChoices.choices, default=PriorityChoices.LOW)
    category = models.CharField(max_length=2, choices=CategoryChoices.choices, default=CategoryChoices.HOME)
    date_created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
