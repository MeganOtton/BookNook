from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Account
from Store.models import BookStorePage
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm

# Profile detailed view
# This view displays the user's profile page
# It displays the user's purchased games
# It also displays the user's profile information
# It is only accessible to logged in users
class ProfileDetailedView(DetailView, LoginRequiredMixin):
    model = Account
    template_name = "Account/account.html"
    context_object_name = "account"


    def get_object(self):
        return get_object_or_404(Account, user=self.request.user)

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
        if request.method == 'POST':
            user = request.user
            profile = get_object_or_404(Account, user=user)
        else:
            post = get_object_or_404(BookStorePage, booktitle=booktitle)

        if post in profile.purchased_books.all():
            messages.error(request, f"You have already purchased the book: {booktitle}")
            return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}?purchased=true")
        else:
            profile.purchased_books.add(post)
            profile.save()
            messages.success(request, f"You have purchased the book: {booktitle}")
            return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}?purchased=true")
    else :
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
        profile = get_object_or_404(Account, user=user)
        

        if post in profile.purchased_books.all():
            return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}?purchased=true")
        else:
            return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}?purchased=false")
    else:   
        return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}?purchased=false")
    

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})