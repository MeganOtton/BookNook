from django import template

register = template.Library()

@register.filter
def filter_and_sort_by_rating(books):
    # Filter books with average rating >= 4 and sort them in descending order
    filtered_books = [book for book in books if book.average_rating >= 4]
    return sorted(filtered_books, key=lambda x: x.average_rating, reverse=True)


@register.filter
def filter_by_genre(books, genre):
    return [book for book in books if genre in [g.name for g in book.genre.all()]]