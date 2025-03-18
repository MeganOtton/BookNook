from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Profile
from Store.models import BookStorePage
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CustomSignupForm, CustomAuthorSignupForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from datetime import date



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

    def get(self, request, *args, **kwargs):
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
            profile = get_object_or_404(Profile, user=user)
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
        profile = get_object_or_404(Profile, user=user)
        

        if post in profile.purchased_books.all():
            return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}?purchased=true")
        else:
            return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}?purchased=false")
    else:   
        return HttpResponseRedirect(f"{reverse('book_details_list', kwargs={'slug': post.slug})}?purchased=false")