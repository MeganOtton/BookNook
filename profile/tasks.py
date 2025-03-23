from django.utils import timezone
from .models import Profile
from Store.models import BookStorePage

def update_user_visible_books(profile):
    # Get all books
    all_books = BookStorePage.objects.all()

    # Filter out purchased books
    visible_books = all_books.exclude(id__in=profile.purchased_books.all())

    # Filter out hidden books and books with hidden topics
    visible_books = visible_books.exclude(
        id__in=profile.hidden_books.all()
    ).exclude(
        topics__in=profile.hidden_topics.all()
    )

    # If the user is a child, filter out adult books
    if profile.role == 'Child':
        visible_books = visible_books.filter(age_rating__lte=17)

    # Update the visible_books field
    profile.visible_books.set(visible_books)

def check_and_update_user_role(profile):
    today = timezone.now().date()
    if profile.birthdate:
        age = today.year - profile.birthdate.year - ((today.month, today.day) < (profile.birthdate.month, profile.birthdate.day))
        if age >= 18 and profile.role == 'Child':
            profile.role = 'Adult'
            profile.save()
            update_user_visible_books(profile)