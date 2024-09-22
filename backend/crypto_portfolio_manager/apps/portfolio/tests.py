from django.test import TestCase
from apps.portfolio.models import Portfolio, User

class PortfolioModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')

    def test_portfolio_creation(self):
        portfolio = Portfolio.objects.create(user=self.user, balance=1000)
        self.assertEqual(portfolio.user, self.user)
        self.assertEqual(portfolio.balance, 1000)
