from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Article, Newsletter


# Custom user creation with role selection
class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new user with role selection.

    Extends Django's built-in UserCreationForm to include email and role fields.
    Roles include Reader, Editor, Journalist, and test (for development/testing purposes).
    """
    ROLE_CHOICES = (
        ('Reader', 'Reader'),
        ('Editor', 'Editor'),
        ('Journalist', 'Journalist'),
        ('test', 'test'),
    )
    # role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')


class ArticleForm(forms.ModelForm):
    """
    Form for creating and updating articles.

    Includes fields for title, content, and the publisher associated with the article.
    """

    class Meta:
        model = Article
        fields = ['title', 'content', 'publisher']


class NewsletterForm(forms.ModelForm):
    """
    Form for creating newsletters.

    Includes fields for title, content, and the publisher sending the newsletter.
    """

    class Meta:
        model = Newsletter
        fields = ['title', 'content', 'publisher']


class SubscriptionForm(forms.ModelForm):
    """
    Form used by Reader users to subscribe to publishers and journalists.

    Provides multiple choice options via checkboxes for selecting subscriptions.
    """

    class Meta:
        model = CustomUser
        fields = ['subscribed_publishers', 'subscribed_journalists']
        widgets = {
            'subscribed_publishers': forms.CheckboxSelectMultiple,
            'subscribed_journalists': forms.CheckboxSelectMultiple,
        }
