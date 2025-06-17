from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from django.urls import reverse
from .models import Article, Newsletter, CustomUser, Publisher
from .forms import (
    CustomUserCreationForm,
    ArticleForm,
    NewsletterForm,
    SubscriptionForm,
)
from django.contrib.auth import logout
from django.contrib import messages


# Role check helpers
def is_journalist(user):
    """Check if the user is in the Journalist group."""
    return user.groups.filter(name='Journalist').exists()


def is_editor(user):
    """Check if the user is in the Editor group."""
    return user.groups.filter(name='Editor').exists()


def is_reader(user):
    """Check if the user is in the Reader group."""
    return user.groups.filter(name='Reader').exists()


# Home Page
def home_view(request):
    """Render the homepage."""
    return render(request, 'newsapp/home.html')


# Registration
def register_view(request):
    """
    Handle user registration and assign them to a selected group.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            try:
                group = Group.objects.get(name=role)
                user.groups.add(group)
            except Group.DoesNotExist:
                messages.warning(request, f"The group '{role}' does not exist.")
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! You are now registered as a {role}.")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def some_view(request):
    """
    Example view to demonstrate template rendering with user role context.
    """
    is_journalist = request.user.groups.filter(name='Journalist').exists()
    return render(request, 'newsapp/some_template.html', {'is_journalist': is_journalist})


# Login
def login_view(request):
    """
    Authenticate and log in users with the default AuthenticationForm.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}! and Group: {user.groups}")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """Log out the user and redirect to homepage."""
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')


# Dashboard
def dashboard_view(request):
    """Render the user dashboard page."""
    return render(request, 'newsapp/dashboard.html')


# Reader Subscriptions
@user_passes_test(is_reader)
def manage_subscriptions(request):
    """
    Allow readers to manage their subscriptions to publishers or journalists.
    """
    user = request.user
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Subscriptions updated successfully.")
            return redirect('dashboard')
    else:
        form = SubscriptionForm(instance=user)
    return render(request, 'newsapp/subscriptions.html', {'form': form})


# Article Views
def article_list_view(request):
    """
    List articles based on user role (Reader, Editor, or Journalist).
    """
    if is_reader(request.user):
        articles = Article.objects.filter(approved=True)
    elif is_editor(request.user):
        articles = Article.objects.all()
    elif is_journalist(request.user):
        articles = Article.objects.filter(author=request.user)
    else:
        return HttpResponseForbidden()
    return render(request, 'newsapp/article_list.html', {'articles': articles})


def article_detail_view(request, pk):
    """
    Display article detail page if user is authorized.
    """
    article = get_object_or_404(Article, pk=pk)
    if article.approved or is_editor(request.user) or article.author == request.user:
        return render(request, 'newsapp/article_detail.html', {'article': article})
    messages.error(request, "You do not have permission to access this page.")
    return redirect('dashboard')


@user_passes_test(is_journalist)
def article_create_view(request):
    """
    Allow journalists to create and submit a new article.
    """
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'newsapp/article_create.html', {'form': form})


def article_update_view(request, pk):
    """
    Allow the article author or an editor to update an article.
    """
    article = get_object_or_404(Article, pk=pk)
    if request.user == article.author or is_editor(request.user):
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('article_list')
        else:
            form = ArticleForm(instance=article)
        return render(request, 'newsapp/article_update.html', {'form': form})
    return HttpResponseForbidden()


def article_delete_view(request, pk):
    """
    Allow the article author or an editor to delete an article.
    """
    article = get_object_or_404(Article, pk=pk)
    if request.user == article.author or is_editor(request.user):
        if request.method == 'POST':
            article.delete()
            messages.success(request, "Article deleted successfully.")
            return redirect('article_list')
        return render(request, 'newsapp/article_delete.html', {'article': article})
    else:
        messages.error(request, "You do not have permission to delete this article.")
        return redirect('article_list')


def article_approve_view(request, pk):
    """
    Allow editors to approve an article.
    """
    article = get_object_or_404(Article, pk=pk)
    article.approved = True
    article.save()
    return redirect('article_list')


@user_passes_test(is_journalist)
def newsletter_create_view(request):
    """
    Allow journalists to create and submit a newsletter.
    """
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            return redirect('newsletter_list')
    else:
        form = NewsletterForm()
    return render(request, 'newsapp/newsletter_create.html', {'form': form})


# Newsletter Views
def newsletter_list_view(request):
    """
    List newsletters based on user role (Reader, Editor, or Journalist).
    """
    if is_reader(request.user):
        newsletters = Newsletter.objects.filter(published=True)
    elif is_editor(request.user):
        newsletters = Newsletter.objects.all()
    elif is_journalist(request.user):
        newsletters = Newsletter.objects.filter(author=request.user)
    else:
        return HttpResponseForbidden()
    return render(request, 'newsapp/newsletter_list.html', {'newsletters': newsletters})


@login_required
def newsletter_update_view(request, pk):
    """
    Allow editors or the newsletter author to update a newsletter.
    """
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if is_editor(request.user) or request.user == newsletter.author:
        if request.method == 'POST':
            form = NewsletterForm(request.POST, instance=newsletter)
            if form.is_valid():
                form.save()
                return redirect('newsletter_list')
        else:
            form = NewsletterForm(instance=newsletter)
        return render(request, 'newsapp/newsletter_create.html', {'form': form})
    return HttpResponseForbidden()


@login_required
def newsletter_delete_view(request, pk):
    """
    Allow editors or the newsletter author to delete a newsletter.
    """
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if is_editor(request.user) or request.user == newsletter.author:
        newsletter.delete()
        return redirect('newsletter_list')
    return HttpResponseForbidden()

# def error_403_view(request, exception=None):
#     """Render a custom 403 Forbidden error page."""
#     return render(request, 'newsapp/error_403.html', status=403)
