from celery import shared_task
from django.utils import timezone
from .models import RebalanceSchedule
from .services import execute_rebalancing_strategy

@shared_task
def rebalance_portfolios():
    now = timezone.now()
    schedules = RebalanceSchedule.objects.filter(next_run__lte=now)
    for schedule in schedules:
        strategy = schedule.strategy
        execute_rebalancing_strategy(strategy)
        if schedule.frequency == 'daily':
            schedule.next_run += timezone.timedelta(days=1)
        elif schedule.frequency == 'weekly':
            schedule.next_run += timezone.timedelta(weeks=1)
        elif schedule.frequency == 'monthly':
            schedule.next_run += timezone.timedelta(days=30)
        schedule.save()
