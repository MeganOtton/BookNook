from django.db import models
from Store.models import BookStorePage
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Account (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userprofile')
    purchased_books = models.ManyToManyField(BookStorePage, related_name='purchased_books', blank=True)
    birthdate = models.DateField(null=True, blank=True, verbose_name="Birthdate")

    # Role field (default is 'adult', which will be changed based on age)
    ACCOUNT_TYPE_CHOICES = [
        ('child', 'Child Reader'),
        ('adult', 'Adult Reader'),
    ]
    role = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, default='adult')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.birthdate:
            # Calculate age based on the birthdate
            today = timezone.now().date()
            age = today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
            
            # Set role based on age
            if age < 18:
                self.role = 'child'
            else:
                self.role = 'adult'
        
        super().save(*args, **kwargs)

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