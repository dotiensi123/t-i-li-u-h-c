from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    address = models.TextField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}'s profile"
