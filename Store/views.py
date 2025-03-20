from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import BookStorePage, Comment
from .forms import RatingForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from profile.models import Profile
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import Genre

# Create your views here.
class BookList(generic.ListView):
    queryset = BookStorePage.objects.filter(status=1)
    context_object_name = 'book_list'
    template_name = "store/index.html"
    paginate_by = 6

    def get_queryset(self):
        queryset = BookStorePage.objects.filter(status=1)
        
        if self.request.user.is_authenticated:
            # Exclude hidden books for the authenticated user
            queryset = queryset.exclude(hidden_by_books=self.request.user.profile)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            purchased_books = profile.purchased_books.all()

            # Count genres
            genre_counts = Genre.objects.filter(books__in=purchased_books).annotate(
                count=Count('books')
            ).order_by('-count')

            # Find the most common genre(s)
            if genre_counts.exists():
                max_count = genre_counts.first().count
                top_genres = genre_counts.filter(count=max_count)
                
                if top_genres.count() == 1:
                    favorite_genre = top_genres.first()
                    # Update the favorite_genre in the Profile model
                    if profile.favorite_genre != favorite_genre:
                        profile.favorite_genre = favorite_genre
                        profile.save()
                else:
                    favorite_genre = None
            else:
                favorite_genre = None

            # If no favourite genre is found, set it to None in the Profile model
            if favorite_genre is None and profile.favorite_genre is not None:
                profile.favorite_genre = None
                profile.save()

            if favorite_genre:
                recommended_books = BookStorePage.objects.filter(status=1, genre=favorite_genre)[:6]
            else:
                recommended_books = BookStorePage.objects.filter(status=1).order_by('-created_on')[:6]

            context['recommended_books'] = recommended_books
            context['favorite_genre'] = favorite_genre

        return context

    @staticmethod
    def Store(request):
        return render(request, 'store/index.html')


class BookListSearch(generic.ListView):
    model = BookStorePage
    template_name = "store/search.html"
    context_object_name = 'book_list_search'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = BookStorePage.objects.filter(status=1)

        if self.request.user.is_authenticated:
            # Exclude hidden books for the authenticated user
            queryset = queryset.exclude(hidden_by_books=self.request.user.profile)

        if query:
            return queryset.filter(
                Q(booktitle__icontains=query) |
                Q(genre__name__icontains=query) |
                Q(topics__name__icontains=query) |
                Q(authorname__icontains=query)
            ).distinct()
        return BookStorePage.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get books released in the last 5 days
        five_days_ago = timezone.now() - timedelta(days=5)
        new_additions = BookStorePage.objects.filter(
            status=1,
            created_on__gte=five_days_ago
        ).order_by('-created_on')

        context['recommended_books'] = BookStorePage.objects.filter(status=1).order_by('-created_on')[:6]
        context['romance_books'] = BookStorePage.objects.filter(status=1, genre__name='Romance')[:6]
        context['fantasy_books'] = BookStorePage.objects.filter(status=1, genre__name='Fantasy')[:6]
        context['new_additions'] = new_additions[:6]  # Limit to 6 books
        return context

# Submit Comment Form View
def book_details(request, slug):
    queryset = BookStorePage.objects.filter(status=1)
    context_object_name = 'book_list'
    book_details_list = get_object_or_404(queryset, slug=slug)
    comments = book_details_list.comments.all().order_by("-created_on")
    comment_count = book_details_list.comments.filter(approved=True).count()
    template_name = "store/bookpage.html"
    paginate_by = 6

    # Check if the book is hidden by the user
    is_book_hidden = False
    if request.user.is_authenticated:
        is_book_hidden = request.user.profile.hidden_books.filter(id=book_details_list.id).exists()
   
    if request.method == "POST":
        comment_form = RatingForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.bookstorepage = book_details_list
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted'
            )
            return HttpResponseRedirect(reverse('book_details_list', args=[slug]))
    else:
        comment_form = RatingForm()

    return render(
        request,
        "store/bookpage.html",
        {"book": book_details_list,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
        "is_book_hidden": is_book_hidden,  # Add this line
        },  
    )

def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = BookStorePage.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = RatingForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = True
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('book_details_list', args=[slug]))


# Delete comment view
def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = BookStorePage.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('book_details_list', args=[slug]))


def user_reviews(request):
    # Fetch comments made by the logged-in user
    user_reviews = Comment.objects.filter(author=request.user).select_related('bookstorepage')

    # Pass the reviews to the template
    return render(request, 'Account/account.html', {'user_reviews': user_reviews})

def review_detail(request, id):
    # Fetch the specific review based on the ID
    review = get_object_or_404(Comment, id=id)
    return render(request, 'review_detail.html', {'review': review})


@login_required
def profile_view(request):
    user_profile = request.user.profile
    accessible_books = BookStorePage.objects.filter(status=1).exclude(
        hidden_by_books=user_profile
    ).filter(
        age_restriction=False if user_profile.role == 'Child' else True
    )

    context = {
        'profile': user_profile,
        'accessible_books': accessible_books,
    }
    return render(request, 'profile/profile.html', context)