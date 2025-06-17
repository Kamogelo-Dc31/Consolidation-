from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('editor', 'Editor'),
        ('journalist', 'Journalist'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        help_text="Defines the user's role: reader, editor, or journalist."
    )

    # Readers can subscribe to multiple publishers
    subscribed_publishers = models.ManyToManyField(Publisher,blank=True, related_name='subsubers', help_text="Publishers that the user (as a reader) is subscribed to.")

    # Readers can also subscribe to individual journalists (CustomUser instances)
    subscribed_journalists = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='journalist_followers',
        help_text="Journalists that the user (as a reader) is subscribed to."
    )

    # Automatically updated whenever the user is modified
    updated_at = models.DateTimeField(auto_now=True)


    def publisher(self):
        try:
            return Publisher.objects.get(user=self)
        except Publisher.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  

        if self.role == 'journalist':
            self.subscribed_publishers.clear()
            self.subscribed_journalists.clear()


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.CharField(max_length=500, blank=True, null=True)  
    approved = models.BooleanField(default=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        permissions = [
            ('can_publish_article', 'Can publish article'),
        ]

    def __str__(self):
        return f"{self.title} by {self.author}"


class Newsletter(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='newsletters')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='newsletters')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ('can_publish_newsletter', 'Can publish newsletter'),
        ]

    def __str__(self):
        return self.title
