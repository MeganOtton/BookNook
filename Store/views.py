from django.shortcuts import render, get_object_or_404, reverse, redirect
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
import random
import json
from django.core.cache import cache
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Device detection view
def device_detection_view(request):
    if 'device_type' in request.session:
        return redirect('index')
    return render(request, 'store/device_detection.html')

class BookList(generic.ListView):
    context_object_name = 'book_list'
    template_name = "store/index.html"
    paginate_by = 6

    def get_queryset(self):
        if self.request.user.is_authenticated:
            cache_key = f'book_list_user_{self.request.user.id}'
        else:
            cache_key = 'book_list_anonymous'

        queryset = cache.get(cache_key)
        if queryset is None:
            queryset = BookStorePage.objects.filter(status=1)
            if self.request.user.is_authenticated:
                queryset = queryset.exclude(hidden_by_books=self.request.user.profile)
            cache.set(cache_key, queryset, 60 * 15)  # Cache for 15 minutes

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['BookStorePage'] = BookStorePage.objects.filter(status=1)
        context['device_type'] = self.request.session.get('device_type', 1)

        if self.request.user.is_authenticated:
            cache_key = f'context_data_user_{self.request.user.id}'
        else:
            cache_key = 'context_data_anonymous'

        cached_context = cache.get(cache_key)
        if cached_context:
            context.update(cached_context)
            print("Using cached context")
            return context

        all_books = self.get_queryset()
        print(f"Total books in queryset: {all_books.count()}")

        five_days_ago = timezone.now() - timedelta(days=5)
        context['new_additions'] = all_books.filter(created_on__gte=five_days_ago).order_by('-created_on')[:6]
        print(f"New additions: {context['new_additions'].count()}")

        from .templatetags.custom_filters import filter_and_sort_by_rating
        context['popular_books'] = filter_and_sort_by_rating(all_books)[:12]
        print(f"Popular books: {len(context['popular_books'])}")

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            purchased_books = profile.purchased_books.all()
            print(f"Purchased books: {purchased_books.count()}")

            genre_counts = Genre.objects.filter(books__in=purchased_books).annotate(
                count=Count('books')
            ).order_by('-count')
            print(f"Genre counts: {genre_counts.count()}")

            if genre_counts.exists():
                max_count = genre_counts.first().count
                top_genres = genre_counts.filter(count=max_count)
                print(f"Top genres: {top_genres.count()}")
                
                if top_genres.count() == 1:
                    favorite_genre = top_genres.first()
                    if profile.favorite_genre != favorite_genre:
                        profile.favorite_genre = favorite_genre
                        profile.save()
                else:
                    favorite_genre = None
            else:
                favorite_genre = None

            if favorite_genre is None and profile.favorite_genre is not None:
                profile.favorite_genre = None
                profile.save()

            if favorite_genre:
                recommended_books = all_books.filter(genre=favorite_genre).exclude(id__in=purchased_books)[:6]
            else:
                recommended_books = all_books.order_by('-created_on').exclude(id__in=purchased_books)[:6]

            context['recommended_books'] = recommended_books
            context['favorite_genre'] = favorite_genre
            print(f"Recommended books: {recommended_books.count()}")
            print(f"Favorite genre: {favorite_genre}")

        cache.set(cache_key, {
            'new_additions': context['new_additions'],
            'popular_books': context['popular_books'],
            'recommended_books': context.get('recommended_books'),
            'favorite_genre': context.get('favorite_genre')
        }, 60 * 15)  # Cache for 15 minutes

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
        
        # Get all books (or a subset if you prefer)
        all_books = BookStorePage.objects.filter(status=1)

        if self.request.user.is_authenticated:
            user_profile = self.request.user.profile
            # Exclude hidden books for the authenticated user
            all_books = all_books.exclude(hidden_by_books=user_profile)

            # Get all purchased books
            purchased_books = list(user_profile.purchased_books.all())
            
            if purchased_books:
                # Randomly select a purchased book
                random_purchase = random.choice(purchased_books)
                
                context['random_purchase'] = random_purchase
                
                # Get similar books based on genres and topics, excluding purchased books
                similar_books = all_books.filter(
                    Q(genre__in=random_purchase.genre.all()) |
                    Q(topics__in=random_purchase.topics.all())
                ).exclude(
                    id__in=[book.id for book in purchased_books]
                ).distinct()
                
                context['similar_books'] = similar_books[:12]  # Limit to 12 books
                
                # Get all genres and topics of the random purchase
                context['random_purchase_genres'] = random_purchase.genre.all()
                context['random_purchase_topics'] = random_purchase.topics.all()

        # Get books released in the last 5 days
        five_days_ago = timezone.now() - timedelta(days=5)
        new_additions = all_books.filter(created_on__gte=five_days_ago).order_by('-created_on')[:6]

        # Popular books (using the custom filter)
        from .templatetags.custom_filters import filter_and_sort_by_rating
        popular_books = filter_and_sort_by_rating(all_books)[:12]  # Limit to 12 books

        context['book_list'] = all_books  # This is needed for the custom filter in the template
        context['popular_books'] = popular_books
        context['recommended_books'] = all_books.order_by('-created_on')[:6]
        # context['romance_books'] = all_books.filter(genre__name='Romance')[:6]
        # context['fantasy_books'] = all_books.filter(genre__name='Fantasy')[:6]
        context['new_additions'] = new_additions

        return context

# Submit Comment Form View
def book_details(request, slug):
    queryset = BookStorePage.objects.filter(status=1)
    book_details_list = get_object_or_404(queryset, slug=slug)
    comments = book_details_list.comments.all().order_by("-created_on")
    comment_count = book_details_list.comments.filter(approved=True).count()

    # Get similar books
    genres = book_details_list.genre.all()
    topics = book_details_list.topics.all()
    similar_books = BookStorePage.objects.filter(status=1).filter(
        Q(genre__in=genres) | Q(topics__in=topics)
    ).exclude(id=book_details_list.id).distinct()

    # Check if the book is hidden by the user
    is_book_hidden = False
    if request.user.is_authenticated:
        profile = request.user.profile
        is_book_hidden = profile.hidden_books.filter(id=book_details_list.id).exists()
        
        # Exclude hidden books from similar books
        similar_books = similar_books.exclude(hidden_by_books=profile)
        
        # Exclude purchased books from similar books
        similar_books = similar_books.exclude(id__in=profile.purchased_books.all())

    # Apply the slice after all filters have been applied
    similar_books = similar_books[:12]  # Limit to 12 books

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
        {
            "book": book_details_list,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
            "is_book_hidden": is_book_hidden,
            "similar_books": similar_books,
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

def save_device_type(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_device_type = int(data.get('device_type'))
            current_device_type = request.session.get('device_type')
            
            if new_device_type != current_device_type:
                request.session['device_type'] = new_device_type
                return JsonResponse({
                    'message': 'Device type updated',
                    'device_type': new_device_type,
                    'refresh': True
                })
            else:
                return JsonResponse({
                    'message': 'Device type unchanged',
                    'device_type': new_device_type,
                    'refresh': False
                })
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'error': 'Invalid data'}, status=400)
    elif request.method == 'GET':
        device_type = request.session.get('device_type')
        return JsonResponse({'message': device_type})
    return JsonResponse({'error': 'Invalid request'}, status=400)
    

@receiver([post_save, post_delete], sender=BookStorePage)
def invalidate_book_cache(sender, instance, **kwargs):
    cache.delete('book_list_anonymous')
    for user in Profile.objects.all():
        cache.delete(f'book_list_user_{user.user.id}')
        cache.delete(f'context_data_user_{user.user.id}')
    cache.delete('context_data_anonymous')