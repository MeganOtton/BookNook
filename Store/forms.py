from .models import Comment
from django import forms

# Create a form for the Comment model
# This form will be used to create a new comment
# It will be displayed in the post_detail view

class RatingForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1 ★'),
        (2, '2 ★★'),
        (3, '3 ★★★'),
        (4, '4 ★★★★'),
        (5, '5 ★★★★★'),
    ]

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select, label="Rate this book")

    class Meta:
        model = Comment
        fields = ('title','rating','body')  # Include other fields as necessary


# class CommentForm(forms.ModelForm):

#     class Meta:
#         model = Comment
#         fields = ('title','rating','body',)