# newsapp/api_views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer


class SubscribedArticlesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        articles = Article.objects.filter(
            approved=True
        ).filter(
            publisher__in=user.subscribed_publishers.all()
        ) | Article.objects.filter(
            approved=True,
            author__in=user.subscribed_journalists.all()
        )
        serializer = ArticleSerializer(articles.distinct(), many=True)
        return Response(serializer.data)
