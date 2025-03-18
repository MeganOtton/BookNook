from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from Store.models import BookStorePage
import datetime

class Profile(models.Model):
    ROLE_CHOICES = [
        ('Child', 'Child Reader'),
        ('Adult', 'Adult Reader'),
        ('Author', 'Author'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    birthdate_author = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Adult')
    purchased_books = models.ManyToManyField(BookStorePage, related_name='purchased_books', blank=True)
    wishlisted_books = models.ManyToManyField(BookStorePage, related_name='wishlisted_books', blank=True)

    def save(self, *args, **kwargs):
        if self.birthdate:
            today = datetime.date.today()
            age = today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
            if age < 18:
                self.role = 'Child'
            else:
                self.role = 'Adult'
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.birthdate_author:
            self.role = 'Author'
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

class CustomShelf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(BookStorePage)
    def __str__(self):
        return f"{self.user.username}'s shelf: {self.name}"


