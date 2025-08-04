from rest_framework.response import Response
from rest_framework import status
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from dotenv import load_dotenv
import os

load_dotenv()
def create_response(success,data=None,status=status.HTTP_500_INTERNAL_SERVER_ERROR):
    return Response({"data":data,"success":success},status=status)

@shared_task
def send_mail_worker(subject,message,reciepient_list):
    try:
        send_mail(subject,message,settings.EMAIL_HOST_USER,reciepient_list)
        return create_response(True,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return create_response(False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from twilio.rest import Client

@shared_task
def send_sms_worker(to,body):
    try:
        client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_ACCOUNT_AUTH_TOKEN'))
        message = client.messages.create(
            body=body,
            from_='+12695207872',
            to=to
        )
        return create_response(True,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return create_response(False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)