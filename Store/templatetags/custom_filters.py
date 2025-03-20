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

@register.filter
def can_access_book(profile, book):
    return profile.can_access_book(book)

@register.filter
def filter_accessible_books(books, profile):
    return [book for book in books if profile.can_access_book(book)]

@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(str(key), False)  # Default to False if key not found

@register.filter
def exclude_hidden_topics(books, user_profile):
    return [book for book in books if not any(topic in user_profile.hidden_topics.all() for topic in book.topics.all())]