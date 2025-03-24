from django import template 
from django.db.models import Avg, F, Q, Prefetch
from Store.models import BookStorePage, Genre
from django.utils import timezone
from datetime import timedelta
from collections import OrderedDict

register = template.Library()

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
def group_by_genre_no_auth(books=None):
    # Define the order of genres you want (without "Popular")
    genre_order = ['Fantasy', 'Romance', 'Mystery', 'Thriller', 'Science Fiction', 'Non-Fiction']
    
    # Get all BookStorePages with status=1 (assuming 1 means published)
    books = BookStorePage.objects.filter(status=1)

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
    
    # Remove empty genres
    genre_groups = OrderedDict((k, v) for k, v in genre_groups.items() if v)
    
    return genre_groups

@register.filter
def filter_and_sort_by_rating_search(books):
    # Annotate books with average rating
    books_with_ratings = books.annotate(avg_rating=Avg('comments__rating'))

    # Filter books with average rating >= 4 or no rating
    filtered_books = books_with_ratings.filter(Q(avg_rating__gte=4) | Q(avg_rating__isnull=True))

    # Order the books by average rating in descending order, with unrated books at the end
    return filtered_books.order_by(F('avg_rating').desc(nulls_last=True))