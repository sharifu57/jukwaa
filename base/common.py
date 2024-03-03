import random
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string 
from django.http import HttpResponse
from base.models import Profile

def get_otp_number():
    otp = random.randint(1000, 9999)
    return otp


def get_random_number():
    projectId = random.randint(1000000,99999999)
    return projectId

def send_otp_email(user_id):
    print("==============initail stage")
    print("===============user id", user_id)
    try:
        user = User.objects.get(id=user_id)
        print("___________________________________user", user)
        profile = Profile.objects.filter(user=user).first()
    except User.DoesNotExist:
        return Response({'status': 400})
    
    otp = profile
    email = user.email

    print("================otp", otp)

    subject = "Activation Code"
    message = render_to_string('acc_active_email.html', {  
        'user': user, 
    }) 
    to_email = email
    send_mail(
        subject,
        message,
        "noreply@gmail.com",
        [to_email],
        fail_silently=False,
    )
    return HttpResponse('Please Confirm your email address') 
    
