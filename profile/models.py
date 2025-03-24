from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from Store.models import BookStorePage, Topic
import datetime
from Store.models import Genre
from django.utils import timezone

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
    hidden_books = models.ManyToManyField(BookStorePage, related_name='hidden_by_books', blank=True)
    hidden_topics = models.ManyToManyField(Topic, related_name='hidden_by_topics', blank=True)
    favorite_genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)

    # New field
    visible_books = models.ManyToManyField(BookStorePage, related_name='visible_to', blank=True)

    def save(self, *args, **kwargs):
        if self.birthdate_author:
            self.role = 'Author'
        elif self.birthdate:
            today = datetime.date.today()
            age = today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
            if age < 18:
                self.role = 'Child'
            else:
                self.role = 'Adult'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    def can_access_book(self, book):
        if self.role == 'Child' and book.age_restriction:
            return False
        return True
    
    def update_visible_books(self):
        all_books = BookStorePage.objects.filter(status=1)
        visible_books = all_books.exclude(
            models.Q(id__in=self.hidden_books.all()) |
            models.Q(topics__in=self.hidden_topics.all())
        )
        if self.role == 'Child':
            visible_books = visible_books.filter(age_restriction=False)
        self.visible_books.set(visible_books)
    
    @staticmethod
    def check_and_update_user_role(profile):
        role_changed = False
        # Check and update user role based on age
        if profile.birthdate:
            age = (timezone.now().date() - profile.birthdate).days // 365
            if age >= 18 and profile.role == 'Child':
                profile.role = 'Adult'
                role_changed = True

        # Update visible books based on role
        all_books = BookStorePage.objects.filter(status=1)
        if profile.role == 'Child':
            visible_books = all_books.filter(age_restriction=False)
        else:  # Adult
            visible_books = all_books  # This includes all books, including those with age restrictions

        if role_changed:
            # If role changed to Adult, set all books as visible
            profile.visible_books.set(all_books)
        else:
            # Remove books that are hidden or have hidden topics only if role didn't change
            visible_books = visible_books.exclude(
                models.Q(id__in=profile.hidden_books.all()) |
                models.Q(topics__in=profile.hidden_topics.all())
            )
            # Update the visible_books
            profile.visible_books.set(visible_books)

        if role_changed:
            profile.save()

        # Call the function in tasks.py to perform additional tasks
        from .tasks import perform_additional_tasks
        perform_additional_tasks(profile)

        return role_changed

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
        Profile.check_and_update_user_role(instance.profile)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    Profile.check_and_update_user_role(instance.profile)

@receiver(m2m_changed, sender=Profile.hidden_books.through)
@receiver(m2m_changed, sender=Profile.hidden_topics.through)
def update_visible_books_on_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        instance.update_visible_books()
        Profile.check_and_update_user_role(instance.profile)