from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from .models import Profile
from Store.models import BookStorePage, Comment, Topic, Genre
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CustomSignupForm, CustomAuthorSignupForm
from datetime import date
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Count

@login_required
def library_view(request):
    return render(request, 'profile/library.html')

class AuthorSignupView(FormView):
    form_class = CustomAuthorSignupForm
    template_name = 'profile/signup_author.html'
    success_url = reverse_lazy('account_login')

    def form_valid(self, form):
        user = form.save(self.request)
        login(self.request, user)
        return super().form_valid(form)

# Profile detailed view
# This view displays the user's profile page
# It displays the user's purchased games
# It also displays the user's profile information
# It is only accessible to logged in users
class ProfileDetailedView(DetailView, LoginRequiredMixin):
    model = Profile
    template_name = "profile/account.html"
    context_object_name = "profile"


    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get_birthdate(self, request, *args, **kwargs):
        self.object = self.get_object()
        role_updated = False
        new_role = None

        if self.object.birthdate:
            today = date.today()
            age = today.year - self.object.birthdate.year - ((today.month, today.day) < (self.object.birthdate.month, self.object.birthdate.day))
            
            new_role = 'Adult' if age >= 18 else 'Child'
            
            if self.object.role != new_role:
                self.object.role = new_role
                self.object.save()
                role_updated = True

        if role_updated:
            messages.info(request, f"Your role has been updated to {new_role} based on your current age.")
            return redirect('profile')  # Assuming 'profile' is the name of your profile URL

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class ProfileAuthorDetailedView(DetailView, LoginRequiredMixin):
    model = Profile
    template_name = "profile/account_author.html"
    context_object_name = "profile_author"


    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

class ProfileAdminDetailedView(DetailView, LoginRequiredMixin):
    model = Profile
    template_name = "profile/account_admin.html"
    context_object_name = "profile_admin"


    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

@login_required
def account_view(request):
    current_user = request.user
    profile = current_user.profile
    hidden_books = profile.hidden_books.all()
    purchased_books = profile.purchased_books.all()
    # all_comments = Comment.objects.all()
    user_comments = Comment.objects.filter(author=current_user).order_by('-created_on')
    
    # Check if the role needs to be updated
    old_role = profile.role
    profile.save()  # This will trigger the save method in the Profile model
    
    role_updated = False
    new_role = None
    
    if old_role != profile.role:
        role_updated = True
        new_role = profile.role

    # Count genres
    genre_counts = Genre.objects.filter(books__in=purchased_books).annotate(
        count=Count('books')
    ).order_by('-count')

    #Find the most common genre(s)
    if genre_counts.exists():
        max_count = genre_counts.first().count
        top_genres = genre_counts.filter(count=max_count)
        
        if top_genres.count() == 1:
            favourite_genre = top_genres.first().name
        else:
            favourite_genre = "No Favourite Genre Found"
    else:
        favourite_genre = "No purchases yet"


    context = {
        'profile': profile,
        # 'all_comments_count': all_comments.count(),
        'user_comments_count': user_comments.count(),
        'user_comments': user_comments,
        'role_updated': role_updated,
        'new_role': new_role,
        'hidden_books': profile.hidden_books.all(),
        'favourite_genre': favourite_genre,
    }
    return render(request, 'profile/account.html', context)

# Function to move a game to the user's purchased games
# This function is called when a user clicks the purchase button
# It adds the game to the user's purchased games
# It also displays a message to the user
# It redirects the user to the game detail page

# If the user is not logged in, it displays a message to the user
# It redirects the user to the game detail page

def move_book_to_chosen(request, booktitle):
    post = get_object_or_404(BookStorePage, booktitle=booktitle)
    if request.user.is_authenticated:
        user = request.user
        profile = get_object_or_404(Profile, user=user)

        if post in profile.purchased_books.all():
            messages.error(request, f"You have already purchased the book: {booktitle}")
        else:
            profile.purchased_books.add(post)
            
            # Check if the book is in the wishlist and remove it
            if post in profile.wishlisted_books.all():
                profile.wishlisted_books.remove(post)
                messages.info(request, f"{booktitle} has been removed from your wishlist as you've purchased it.")
            
            profile.save()
            messages.success(request, f"You have purchased the book: {booktitle}")
        
        return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}")
    else:
        messages.error(request, f'Please Sign In to purchase: {booktitle}')
    
    return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}")


# Function to check if the user owns the game
# This function is called when a user views a game detail page
# It checks if the user owns the game
# It redirects the user to the game detail page

# If the user owns the game, it adds a query parameter to the URL
# The query parameter is used to display a message to the user
# If the user does not own the game, it adds a query parameter to the URL
# The query parameter is used to display a message to the user

# If the user is not logged in, it adds a query parameter to the URL
# The query parameter is used to display a message to the user
# It redirects the user to the game detail page

# The function returns an HTTP response
# The HTTP response contains the URL of the game detail page
# The URL contains the query parameter
# The query parameter is used to display a message to the user
def check_book_ownership(request, booktitle):
    post = get_object_or_404(BookStorePage, booktitle=booktitle)
    if request.user.is_authenticated:
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        

        if post in profile.purchased_books.all():
            return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}")
        else:
            return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}")
    else:   
        return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}")

    
# Function to move a game to the user's purchased games
# This function is called when a user clicks the purchase button
# It adds the game to the user's purchased games
# It also displays a message to the user
# It redirects the user to the game detail page

# If the user is not logged in, it displays a message to the user
# It redirects the user to the game detail page

def move_book_to_wishlist(request, booktitle):
    post = get_object_or_404(BookStorePage, booktitle=booktitle)
    if request.user.is_authenticated:
        user = request.user
        profile = get_object_or_404(Profile, user=user)

        if post in profile.purchased_books.all():
            # If the book is already purchased, remove it from wishlist if it's there
            if post in profile.wishlisted_books.all():
                profile.wishlisted_books.remove(post)
                profile.save()
                messages.info(request, f"{booktitle} has been removed from your wishlist as you've already purchased it.")
            else:
                messages.info(request, f"You've already purchased {booktitle}. It can't be added to the wishlist.")
                return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}")
        elif post in profile.wishlisted_books.all():
            profile.wishlisted_books.remove(post)
            profile.save()
            messages.success(request, f"You have removed {booktitle} from your wishlist.")
        else:
            profile.wishlisted_books.add(post)
            profile.save()
            messages.success(request, f"You have added {booktitle} to your wishlist. Click the heart again to remove it.")
        
        return HttpResponseRedirect(reverse('book_details_list', kwargs={'slug': post.slug}))
    else:
        messages.error(request, f'Please Sign In to update your wishlist.')
    
    return HttpResponseRedirect(reverse('book_details_list', kwargs={'slug': post.slug}))

@login_required
def library_view(request):
    user_profile = Profile.objects.get(user=request.user)
    purchased_books = user_profile.purchased_books.all()
    wishlisted_books = user_profile.wishlisted_books.all()
    context = {
        'purchased_books': purchased_books,
        'wishlisted_books': wishlisted_books,
    }
    return render(request, 'profile/library.html', context)


@login_required
def hide_options(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(BookStorePage, id=book_id)
        user_profile = request.user.profile
        
        if 'hide_book' in request.POST:
            user_profile.hidden_books.add(book)
            messages.success(request, f"{book.booktitle} has been hidden.")
        else:
            user_profile.hidden_books.remove(book)
            messages.success(request, f"{book.booktitle} has been unhidden.")

        hidden_topics = request.POST.getlist('hide_topics')
        for topic in book.topics.all():
            if str(topic.id) in hidden_topics:
                user_profile.hidden_topics.add(topic)
            else:
                user_profile.hidden_topics.remove(topic)

        user_profile.save()

        # Redirect back to the book page
        return redirect('book_details_list', slug=book.slug)

    # If not POST, redirect to the book page
    return redirect('book_details_list', slug=book.slug)


