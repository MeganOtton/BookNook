from django.contrib import admin
from .models import BookStorePage, Genre, Topic


# Register your models here.
@admin.register(BookStorePage)
class BookStorePageAdmin(admin.ModelAdmin):
    list_display = ('booktitle', 'authorname', 'bookprice', 'bookrating', 'status')
    filter_horizontal = ('genre','topics')  # Better interface for selecting multiple genres
    search_fields = ('booktitle', 'authorname', 'bookprice', 'bookrating')
    prepopulated_fields = {'slug': ('booktitle',)}
    ordering = ['status' ]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Topic)
class TopicsAdmin(admin.ModelAdmin):
    list_display = ('name',)