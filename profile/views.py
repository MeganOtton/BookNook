from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Profile
from Store.models import BookStorePage, Comment
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CustomSignupForm, CustomAuthorSignupForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from datetime import date
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
from .models import CustomShelf



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
    
    # Check if the role needs to be updated
    old_role = profile.role
    profile.save()  # This will trigger the save method in the Profile model
    
    role_updated = False
    new_role = None
    
    if old_role != profile.role:
        role_updated = True
        new_role = profile.role

    # Fetch all comments
    all_comments = Comment.objects.all()
    
    # Fetch user's comments
    user_comments = Comment.objects.filter(author=current_user).select_related('bookstorepage').order_by('-created_on')

    # Debug information
    print(f"Current user: {current_user.username}")
    print(f"Total comments: {all_comments.count()}")
    print(f"User comments: {user_comments.count()}")
    for comment in user_comments:
        print(f"Comment {comment.id}: Book: {comment.bookstorepage.booktitle}, Content: {comment.body[:50]}...")

    context = {
        'profile': profile,
        'all_comments_count': all_comments.count(),
        'user_comments_count': user_comments.count(),
        'user_comments': user_comments,
        'role_updated': role_updated,
        'new_role': new_role,
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
        
        return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}?purchased=true")
    else:
        messages.error(request, f'Please Sign In to purchase: {booktitle}')
    
    return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}?purchased=false")


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
            return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}?purchased=true")
        else:
            return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}?purchased=false")
    else:   
        return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}?purchased=false")

    
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
                return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}?purchased=true")
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
    user_shelves = CustomShelf.objects.filter(user=request.user)
    context = {
        'purchased_books': purchased_books,
        'wishlisted_books': wishlisted_books,
        'user_shelves': user_shelves,
    }
    return render(request, 'profile/library.html', context)




@require_POST
@login_required
def create_shelf(request):
    if request.method == 'POST':
        shelf_name = request.POST.get('shelf_name')
        # Create the shelf in your database
        new_shelf = CustomShelf.objects.create(name=shelf_name, user=request.user)
        return JsonResponse({'success': True, 'shelf_id': new_shelf.id, 'shelf_name': new_shelf.name})
    return JsonResponse({'success': False}, status=400)

@require_POST
@login_required
def assign_book_to_shelf(request):
    shelf_id = request.POST.get('shelf_id')
    book_id = request.POST.get('book_id')
    try:
        shelf = CustomShelf.objects.get(id=shelf_id, user=request.user)
        book = BookStorePage.objects.get(id=book_id)
        shelf.books.add(book)
        return JsonResponse({'success': True})
    except (CustomShelf.DoesNotExist, BookStorePage.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Shelf or book not found'})
