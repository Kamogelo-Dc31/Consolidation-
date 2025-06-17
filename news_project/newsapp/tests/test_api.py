from rest_framework.test import APITestCase
from django.urls import reverse
from newsapp.models import CustomUser, Publisher, Article
from rest_framework import status


class SubscribedArticlesAPITestCase(APITestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(name='Hyperion News')
        self.reader = CustomUser.objects.create_user(
            username='reader1', password='readerpass', role='reader'
        )
        self.journalist = CustomUser.objects.create_user(
            username='journalist1', password='journalistpass', role='journalist'
        )
        self.unsubscribed_journalist = CustomUser.objects.create_user(
            username='outsider', password='outpass', role='journalist'
        )

        self.article1 = Article.objects.create(
            title="Approved Article",
            content="Visible to reader",
            author=self.journalist,
            publisher=self.publisher,
            approved=True
        )

        self.article2 = Article.objects.create(
            title="Hidden Article",
            content="Not visible to reader",
            author=self.unsubscribed_journalist,
            publisher=self.publisher,
            approved=True
        )

        self.reader.subscribed_publishers.add(self.publisher)
        self.reader.subscribed_journalists.add(self.journalist)

    def test_reader_can_view_subscribed_articles(self):
        self.client.login(username='reader1', password='readerpass')
        url = reverse('subscribed_articles')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Approved Article')

    def test_unauthenticated_access(self):
        url = reverse('subscribed_articles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_article_not_returned_if_not_subscribed(self):
        self.client.login(username='reader1', password='readerpass')
        url = reverse('subscribed_articles')
        response = self.client.get(url)
        titles = [article['title'] for article in response.data]
        self.assertNotIn('Hidden Article', titles)
