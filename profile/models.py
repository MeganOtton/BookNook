from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from Store.models import BookStorePage, Topic
import datetime
from Store.models import Genre
from django.utils import timezone
from django.contrib.auth.signals import user_logged_in

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
    
    #Starts Here!!!!
    @receiver(user_logged_in)
    def update_profile_on_login(sender, user, request, **kwargs):
        profile = Profile.objects.get(user=user)
        Profile.update_visible_books(profile)

    # Visibility updates on book status change
    def update_visible_books(self):
        # Start with all published books
        if self.role == 'Child':
            all_books = set(BookStorePage.objects.filter(status=1, age_restriction=False))
        else:
            all_books = set(BookStorePage.objects.filter(status=1))
        
        # Remove purchased books from visible books
        visible_books = all_books - set(self.purchased_books.all())
        
        # Remove hidden books from visible books
        visible_books -= set(self.hidden_books.all())
        
        # Remove books with hidden topics from visible books
        books_with_hidden_topics = set(BookStorePage.objects.filter(topics__in=self.hidden_topics.all()))
        visible_books -= books_with_hidden_topics
        
        # Update the visible_books field
        self.visible_books.set(visible_books)
        
        # Save the changes
        self.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
        Profile.update_visible_books(instance.profile)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    Profile.update_visible_books(instance.profile)

@receiver(m2m_changed, sender=Profile.hidden_books.through)
@receiver(m2m_changed, sender=Profile.hidden_topics.through)
def update_visible_books_on_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        instance.update_visible_books()