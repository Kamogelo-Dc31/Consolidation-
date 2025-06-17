from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Article, Newsletter


# Custom user creation with role selection
class CustomUserCreationForm(UserCreationForm):
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


# Article create/update form
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'publisher']


# Newsletter create form
class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'content', 'publisher']


# Subscription form for Readers
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['subscribed_publishers', 'subscribed_journalists']
        widgets = {
            'subscribed_publishers': forms.CheckboxSelectMultiple,
            'subscribed_journalists': forms.CheckboxSelectMultiple,
        }
