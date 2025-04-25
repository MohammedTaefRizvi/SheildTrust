from django.utils.timezone import now
from django.core.mail import send_mail
from django.core.cache import cache
from fraud.models import FraudAlerts, FraudAlertEmails


def send_fraud_alerts_emails():
    fraud_alerts= FraudAlerts.objects.filter(alert_sent=False)
    for alerts in fraud_alerts:
        transaction = alerts.transaction
        card= transaction.card
        user=card.user

        subject ="Shield Trust Bank - Fraud Alert: Suspicious Transaction Detected!"
        body = f"""
        Dear {user.name},

        We have detected a **suspicious transaction** on your Shield Trust Bank account.

        **Transaction Details:**
        - **Amount:** {transaction.amount}
        - **Merchant:** {transaction.merchant_name}
        - **Location:** {transaction.location}
        - **Date:** {transaction.date}

        If you recognize this transaction, no action is needed.  
        If **this was not you**, please **report it immediately** by contacting our support team.

        Shield Trust Bank prioritizes your security.  

        Regards,  
        **Shield Trust Bank - Fraud Detection Team**
        """

        try:
            send_mail(
                subject,
                body,
                "noreply@shieldtrustbank.com",
                [user.email],
                fail_silently=False
            )

            FraudAlertEmails.objects.create(
                user=user,
                alert=alerts,
                email_subject=subject,
                email_body = body,
                sent_at=now().date()
            )
            alerts.alert_sent = True  # Ensure field name matches model
            alerts.sent_timestamp = now().date()
            alerts.save(update_fields=['alert_sent', 'sent_timestamp'])

            print(f"email send - {alerts.id}")
        except Exception as e:
            print(f"failed email {e}")