from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_welcome_email(user_email, username):
    """
    Send welcome email to newly registered users
    """
    try:
        subject = 'Welcome to Our Django API!'
        message = f'''
        Hello {username},

        Welcome to our Django REST API project!
        
        Your account has been successfully created.
        
        You can now access our API endpoints and explore the features.
        
        Best regards,
        Django API Team
        '''
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )
        
        logger.info(f"Welcome email sent successfully to {user_email}")
        return f"Email sent to {user_email}"
        
    except Exception as e:
        logger.error(f"Failed to send email to {user_email}: {str(e)}")
        return f"Failed to send email: {str(e)}"

@shared_task
def process_data_task(data):
    """
    Example background task for processing data
    """
    import time
    time.sleep(10)  # Simulate long processing
    return f"Processed data: {data}"