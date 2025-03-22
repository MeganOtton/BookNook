from django.contrib import admin
from django.db import models
from django.forms import Textarea
from .models import BookStorePage, Genre, Topic, Comment


# Register your models here.
@admin.register(BookStorePage)
class BookStorePageAdmin(admin.ModelAdmin):
    list_display = ('booktitle', 'authorname', 'bookprice', 'status')
    filter_horizontal = ('genre','topics')  # Better interface for selecting multiple genres
    search_fields = ('booktitle', 'authorname', 'bookprice')
    prepopulated_fields = {'slug': ('booktitle',)}
    ordering = ['status' ]
    formfield_overrides = {
        models.CharField: {'widget': admin.widgets.AdminTextInputWidget(attrs={'size': '100'})},
        models.CharField: {
            'widget': Textarea(attrs={'rows': 10, 'cols': 100}),
        },
    }

    class Media:
        js = ('js/char_count.js',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Topic)
class TopicsAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Register your models here.
admin.site.register(Comment)
