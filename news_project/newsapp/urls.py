from django.urls import path, include
#from django.contrib.auth import views as auth_views
from newsapp.views import home_view
from django.urls import path
from . import views
from .views import some_view
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from .views import article_list_view

urlpatterns = [
    path('', home_view, name='home'),  # Landing/home page
    path('login/', LoginView.as_view, name='logout'),
    # Make change to logout according to E-commece project
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('api/', include('newsapp.api_urls')),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('news/register/', views.register_view, name='register'),
    path('news/subscriptions/', views.manage_subscriptions, name='subscriptions'),
    path('some/', some_view, name='some_view'),

    # API
    path('api/', include('newsapp.api_urls')),

    # Article URLs
    # path('news/articles/', views.article_list_view, name='article_list'),
    path('news/articles/', article_list_view, name='article_list'),

    path('articles/<int:pk>/', views.article_detail_view, name='article_detail'),
    path('news/articles/create/', views.article_create_view, name='article_create'),
    path('news/articles/<int:pk>/delete/', views.article_delete_view, name='article_delete'),
    path('news/articles/<int:pk>/edit/', views.article_update_view, name='article_update'),
    path('news/articles/<int:article_id>/approve/', views.article_approve_view, name='approve_article'),

    # Newsletter URLs
    path('newsletters/create/', views.newsletter_create_view, name='newsletter_create'),
    path('newsletters/<int:pk>/update/', views.newsletter_update_view, name='newsletter_update'),
    path('newsletters/<int:pk>/delete/', views.newsletter_delete_view, name='newsletter_delete'),
    path('newsletters/', views.newsletter_list_view, name='newsletter_list'),
]
