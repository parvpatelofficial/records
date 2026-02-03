from django.db import models
from django.conf import settings
from accounts.models import Principal

class ActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"

class YearlyReport(models.Model):
    principal = models.ForeignKey(Principal, on_delete=models.CASCADE)
    year = models.IntegerField()
    pdf_file = models.FileField(upload_to='yearly_reports/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report {self.year}"
