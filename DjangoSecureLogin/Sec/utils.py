from .models import ActivityLog

def log_activity(user, activity_description):
    ActivityLog.objects.create(user=user, activity=activity_description)