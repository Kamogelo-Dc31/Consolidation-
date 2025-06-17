# newsapp/serializers.py
from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    related = serializers.PrimaryKeyRelatedField(read_only=True)
    # Or, if you want nested data:
    # related = ArticleSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
