from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from newsapp.models import Article, Newsletter


def setup_journalist_permissions():
    journalist_group, created = Group.objects.get_or_create(name='Journalist')

    # Standard model permissions
    permissions = [
        'add_article', 'change_article', 'delete_article', 'view_article',
        'add_newsletter', 'change_newsletter', 'delete_newsletter', 'view_newsletter',
        'can_publish_article', 'can_publish_newsletter'
    ]

    for codename in permissions:
        try:
            if 'article' in codename:
                content_type = ContentType.objects.get_for_model(Article)
            else:
                content_type = ContentType.objects.get_for_model(Newsletter)
            permission = Permission.objects.get(codename=codename, content_type=content_type)
            journalist_group.permissions.add(permission)
        except Permission.DoesNotExist:
            print(f"Permission '{codename}' does not exist.")

    print("Journalist permissions assigned.")
