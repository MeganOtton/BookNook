from django.db import models
from Store.models import BookStorePage
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Account (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userprofile')
    purchased_books = models.ManyToManyField(BookStorePage, related_name='purchased_books', blank=True)

    def __str__(self):
        return self.user.username

# Create or update the user profile
# This function creates or updates the user profile
# It is called when a user is created or updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        Account.objects.create(user=instance)