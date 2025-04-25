from django.core.cache import cache
from django.db import connection
from apscheduler.schedulers.background import BackgroundScheduler

from .models import Transaction
from .ml_model import predict_fraud

def predict():
    if not connection.introspection.table_names():
        return
    total_transaction = cache.get('total_transaction', 0)
    now_transaction = Transaction.objects.count()

    if total_transaction < now_transaction:
        new_transactions = Transaction.objects.all().order_by('transaction_id')[total_transaction:]
        for transaction in new_transactions:
            predict_fraud(transaction.transaction_id)
        cache.set('total_transaction', now_transaction, timeout=None)

    print("Checked transactions:", cache.get('total_transaction'))

def start_schedular():
    scheduler = BackgroundScheduler()
    scheduler.add_job(predict, "interval", seconds=90)
    scheduler.start()
