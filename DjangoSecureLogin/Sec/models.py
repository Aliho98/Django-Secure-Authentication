from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.utils import timezone


class CustomUser(AbstractUser):
    SecurityQuestion = models.CharField(max_length=100)
    SecurityQuestionAnswer = models.CharField(max_length=100)
    # Store hashed passwords in a comma-separated list
    passwords_history = models.TextField(default='', blank=True)

    def set_password(self, raw_password):
        """
        Override Django's set_password method to store password history
        """
        previous_passwords = self.passwords_history.split(',') if self.passwords_history else []
        hashed_password = make_password(raw_password)

        if hashed_password not in previous_passwords:
            # Ensure the new password is not in the history
            previous_passwords.append(hashed_password)
            # Limit the history size to 10, for example
            previous_passwords = previous_passwords[-10:]
            self.passwords_history = ','.join(previous_passwords)
            super().set_password(raw_password)
        else:
            # Password is in the history, raise an error or handle accordingly
            raise ValueError("Cannot reuse a previous password.")

    def reset_password(self, raw_password):
        """
        Custom method for resetting the password
        """
        hashed_password = make_password(raw_password)
        previous_passwords = self.passwords_history.split(',') if self.passwords_history else []

        # Update the history only if the new password is not in the history
        if hashed_password not in previous_passwords:
            previous_passwords.append(hashed_password)
            # Limit the history size to 10, for example
            previous_passwords = previous_passwords[-10:]
            self.passwords_history = ','.join(previous_passwords)
        
        super().set_password(raw_password)
    
    def check_password(self, raw_password):
        """
        Override Django's check_password method to compare against password history
        """
        if any(make_password(raw_password) == hashed for hashed in self.passwords_history.split(',')):
            return True
        return super().check_password(raw_password)




class ActivityLog(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    
    # Add more fields as per your logging needs

    def __str__(self):
        return f"{self.activity} by {self.user} at {self.timestamp}"