from django.db import models
from django.contrib.auth.models import User

# Employee Table
class Employee(models.Model):
    POSITION_CHOICES = [
        ("HR", "HR"),
        ("Manager", "Manager"),
        ("Team Leader", "Team Leader"),
        ("Employee", "Employee"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    emp_id = models.CharField(max_length=20, unique=True)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.emp_id} - {self.user.username}"


# Score History Table
class ScoreHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="history")
    added_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="added_scores")
    score_added = models.IntegerField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.emp_id} - +{self.score_added}"
