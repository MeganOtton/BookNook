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
        Profile.check_and_update_user_role(profile)

    #2nd place
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
            Profile.remove_purchased_from_visible(profile)
        else:  # Adult
            visible_books = all_books  # This includes all books, including those with age restrictions
            Profile.remove_purchased_from_visible(profile)

        if role_changed:
            profile.save()

        return role_changed
    
    #3rd place
    def remove_purchased_from_visible(self):
        # Get the set of purchased books
        purchased_books = set(self.purchased_books.all())
        
        # Get the current set of visible books
        visible_books = set(self.visible_books.all())
        
        # Remove purchased books from visible books
        updated_visible_books = visible_books - purchased_books
        
        # Update the visible_books field
        self.visible_books.set(updated_visible_books)

        # Call the remove_hidden_from_visible method
        self.remove_hidden_from_visible()
    
    #4th place
    def remove_hidden_from_visible(self):
        print("remove_hidden_from_visible")
        # Get the set of hidden books
        hidden_books = set(self.hidden_books.all())
        
        # Get the set of purchased books
        purchased_books = set(self.purchased_books.all())
        
        # Get the current set of visible books
        visible_books = set(self.visible_books.all())
        
        # Remove both hidden and purchased books from visible books
        updated_visible_books = visible_books - (hidden_books | purchased_books)

        # Call the new method to remove books with hidden topics
        updated_visible_books = self.remove_hidden_topics_from_visible(updated_visible_books)
        
        # Update the visible_books field
        self.visible_books.set(updated_visible_books)

    #5th place
    def remove_hidden_topics_from_visible(self, visible_books):
        print("remove_hidden_topics_from_visible")
        # Get the set of books with hidden topics
        books_with_hidden_topics = set(BookStorePage.objects.filter(topics__in=self.hidden_topics.all()))
        
        # Remove books with hidden topics from visible books
        updated_visible_books = visible_books - books_with_hidden_topics
        
        return updated_visible_books

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