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
    else:
        visible_books = visible_books.filter(age_rating__lte=99)

    # Update the visible_books field
    profile.visible_books.set(visible_books)