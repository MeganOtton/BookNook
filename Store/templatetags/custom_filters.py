from django import template
from profile.models import Profile  
from django.db.models import Q
from Store.models import BookStorePage, Genre

register = template.Library()

@register.filter
def filter_and_sort_by_rating(books):
    # Filter books with average rating >= 4 and sort them in descending order
    filtered_books = [book for book in books if book.average_rating >= 4]
    
    # If no books have a rating of 4 or higher, use all books
    if not filtered_books:
        filtered_books = books
    
    # Sort the books by average rating in descending order
    return sorted(filtered_books, key=lambda x: x.average_rating or 0, reverse=True)

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