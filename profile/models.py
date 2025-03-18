from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from Store.models import BookStorePage
import datetime

class Profile(models.Model):
    ROLE_CHOICES = [
        ('child', 'Child Reader'),
        ('adult', 'Adult Reader'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='adult')
    purchased_books = models.ManyToManyField(BookStorePage, related_name='purchased_books', blank=True)

    def save(self, *args, **kwargs):
        if self.birthdate:
            today = datetime.date.today()
            age = today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
            if age < 18:
                self.role = 'child'
            else:
                self.role = 'adult'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()