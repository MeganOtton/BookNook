from .models import Comment
from django import forms

class RatingForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1 ★'),
        (2, '2 ★★'),
        (3, '3 ★★★'),
        (4, '4 ★★★★'),
        (5, '5 ★★★★★'),
    ]

    rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        coerce=int,
        widget=forms.Select,
        label="Rate this book"
    )

    class Meta:
        model = Comment
        fields = ('title', 'rating', 'body')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['rating'] = self.instance.rating