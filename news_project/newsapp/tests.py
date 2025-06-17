from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from newsapp.models import Journalist, Publisher, Newsletter

User = get_user_model()

class NewsletterCreateTest(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.user = User.objects.create_user(username="journalist", password="testpass")
        self.journalist = Journalist.objects.create(user=self.user, publisher=self.publisher)

    def test_journalist_can_create_newsletter(self):
        self.client.login(username="journalist", password="testpass")
        response = self.client.post(reverse('newsletter_create'), {
            'title': 'Test Newsletter',
            'content': 'This is a test newsletter.',
        })
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard
        newsletter = Newsletter.objects.first()
        self.assertIsNotNone(newsletter)
        self.assertEqual(newsletter.title, 'Test Newsletter')
        self.assertEqual(newsletter.publisher, self.publisher)

# Create your tests here.
