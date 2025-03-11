from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Store'

    # def ready(self):
    #     from .models import Genre
    #     predefined_genres = [
    #         ('fantasy', 'Fantasy'),
    #         ('sci_fi', 'Science Fiction'),
    #         ('romance', 'Romance'),
    #         ('mystery', 'Mystery'),
    #         ('non_fiction', 'Non-Fiction'),
    #         ('thriller', 'Thriller'),
    #     ]
    #     for key, name in predefined_genres:
    #         Genre.objects.get_or_create(name=key)