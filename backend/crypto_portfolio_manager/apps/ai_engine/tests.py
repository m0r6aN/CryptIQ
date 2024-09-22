from django.test import TestCase
from apps.ai_engine.services import ai_stop_loss_take_profit

class AITests(TestCase):

    def test_ai_stop_loss_take_profit(self):
        result = ai_stop_loss_take_profit(user=None, coin='bitcoin')
        self.assertIn('stop_loss', result)
        self.assertIn('take_profit', result)
        self.assertLess(result['stop_loss'], 0)
        self.assertGreater(result['take_profit'], 0)
