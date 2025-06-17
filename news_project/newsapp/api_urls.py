# newsapp/api_urls.py
from django.urls import path
from .api_views import SubscribedArticlesView

urlpatterns = [
    path('subscribed-articles/', SubscribedArticlesView.as_view(), name='subscribed_articles'),
]
