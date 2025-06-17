from django.contrib import admin
from .models import Article, Publisher, Newsletter, CustomUser

admin.site.register(Article)
admin.site.register(Publisher)
admin.site.register(Newsletter)
admin.site.register(CustomUser)


# Register your models here.
