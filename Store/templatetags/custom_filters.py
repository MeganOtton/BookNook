from django import template
from profile.models import Profile  
from django.db.models import Q
from Store.models import BookStorePage, Genre
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, Prefetch
from collections import OrderedDict

register = template.Library()

from django.db.models import Avg, F, Q

@register.filter
def filter_and_sort_by_rating(books):
    # Annotate books with their average rating
    books_with_ratings = books.annotate(avg_rating=Avg('comments__rating'))

    # Filter books with average rating >= 4
    filtered_books = books_with_ratings.filter(Q(avg_rating__gte=4) | Q(avg_rating__isnull=True))

    # If no books have a rating of 4 or higher, use all books
    if not filtered_books.exists():
        filtered_books = books_with_ratings

    # Order the books by average rating in descending order
    return filtered_books.order_by(F('avg_rating').desc(nulls_last=True))

@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(str(key), False)  # Default to False if key not found

@register.filter
def filter_by_genre(books, genre_or_book):
    # If books is a string (book_list), get all books
    if isinstance(books, str):
        books = BookStorePage.objects.all()
    
    # Convert QuerySet to list if it's not already a list
    if not isinstance(books, list):
        books = list(books)
    
    # Check if genre_or_book is a string (genre name) or a Book object
    if isinstance(genre_or_book, str):
        # It's a genre name
        return [book for book in books if genre_or_book in [g.name for g in book.genre.all()]]
    elif isinstance(genre_or_book, BookStorePage):
        # It's a book object
        genres = genre_or_book.genre.all()
        return [book for book in books if book.id != genre_or_book.id and any(g in genres for g in book.genre.all())]
    else:
        # Invalid input
        return []
    

@register.filter
def filter_by_favorite_genre(books, user):
    if not user.is_authenticated or not user.profile.favorite_genre:
        return []

    favorite_genre = user.profile.favorite_genre
    return [book for book in books if favorite_genre in book.genre.all()]


@register.filter
def filter_status(books, status):
    if hasattr(books, 'filter'):
        # It's a QuerySet
        return books.filter(status=status)
    else:
        # It's likely a list
        return [book for book in books if book.status == status]
    

@register.filter
def filter_new_additions(books):
    seven_days_ago = timezone.now() - timedelta(days=7)
    return [book for book in books if book.created_on >= seven_days_ago]


@register.filter
def filter_new_additions_not_auth(books=None):
    seven_days_ago = timezone.now() - timedelta(days=7)
    return BookStorePage.objects.filter(created_on__gte=seven_days_ago, status=1)


@register.filter
def filter_and_sort_by_rating_not_auth(books=None):
    # Fetch all BookStorePages with status=1 (assuming 1 means published)
    all_books = BookStorePage.objects.filter(status=1)

    # Annotate each book with its average rating
    books_with_ratings = all_books.annotate(avg_rating=Avg('comments__rating'))

    # Filter books with average rating >= 4
    filtered_books = books_with_ratings.filter(avg_rating__gte=4)

    # If no books have a rating of 4 or higher, use all books
    if not filtered_books.exists():
        filtered_books = books_with_ratings

    # Order the books by average rating in descending order
    return filtered_books.order_by('-avg_rating')


from django.db.models import Avg, Prefetch
from collections import OrderedDict
from django.db.models.functions import Coalesce

@register.filter
def group_by_genre(books, user=None):
    # Define the order of genres you want, including "Popular" at the beginning
    genre_order = ['Popular', 'Fantasy', 'Romance', 'Mystery', 'Thriller', 'Science Fiction', 'Non-Fiction']
    
    # Annotate books with average rating and prefetch genres
    books = books.annotate(
        avg_rating=Coalesce(Avg('comments__rating'), 0.0)
    ).prefetch_related(
        Prefetch('genre', queryset=Genre.objects.only('name'))
    )
    
    # Use an OrderedDict to maintain the order
    genre_groups = OrderedDict((genre, []) for genre in genre_order)
    
    # Add "Other" category for genres not in the predefined list
    genre_groups['Other'] = []
    
    # Populate genre groups
    for book in books:
        book_genres = book.genre.all()
        if not book_genres:
            genre_groups['Other'].append(book)
        else:
            for genre in book_genres:
                if genre.name in genre_groups:
                    genre_groups[genre.name].append(book)
                else:
                    genre_groups['Other'].append(book)
    
    # Sort books in each genre by average rating
    for genre in genre_groups:
        genre_groups[genre] = sorted(genre_groups[genre], key=lambda x: x.avg_rating, reverse=True)
    
    # Populate "Popular" category with top-rated books (4 stars or higher) across all genres
    all_books = [book for books in genre_groups.values() for book in books]
    popular_books = sorted([book for book in all_books if book.avg_rating >= 4], key=lambda x: x.avg_rating, reverse=True)[:20]
    genre_groups['Popular'] = popular_books
    
    # Remove empty genres
    genre_groups = OrderedDict((k, v) for k, v in genre_groups.items() if v)
    
    return genre_groups


@register.filter
def group_bookstore_pages_by_genre(books):
    from collections import OrderedDict
    
    # Define the order of genres you want
    genre_order = ['Fantasy', 'Romance', 'Mystery', 'Thriller', 'Science Fiction', 'Non-Fiction']
    
    # Use an OrderedDict to maintain the order
    genre_groups = OrderedDict((genre, []) for genre in genre_order)
    
    # Group books by genre
    for book in books:
        for genre in book.genre.all():
            if genre.name not in genre_groups:
                genre_groups[genre.name] = []
            genre_groups[genre.name].append(book)
    
    # Remove any empty genre groups
    return OrderedDict((k, v) for k, v in genre_groups.items() if v)


@register.filter
def get_recommended_books(books, user):
    if not user.is_authenticated or not user.profile.favorite_genre:
        return []

    favorite_genre = user.profile.favorite_genre
    recommended_books = [book for book in books if favorite_genre in book.genre.all()]
    
    # Sort recommended books by rating
    recommended_books.sort(key=lambda x: x.average_rating or 0, reverse=True)
    
    # Limit to top 10 recommendations
    return recommended_books[:10]