from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from django.db.models.query_utils import Q
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import requests
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

# from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.views import PasswordResetView
from rest_framework.generics import CreateAPIView
from base.models import Category, Profile
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
import random

# Create your views here.


def get_random_number():
    otp = random.randint(1000, 9999)
    return otp


class UserRegisterViewSet(viewsets.GenericViewSet):
    serializer_class = RegisterSerializer
    queryset = User.objects.filter(is_active=True)

    @action(detail=False, methods=["POST"])
    def register(self, request):
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        user_type = request.data.get("user_type")
        category = request.data.get("category")
        phone_number = request.data.get("phone_number")

        if not email or not first_name or not last_name:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Email and Names are required",
                }
            )

        if User.objects.filter(Q(first_name=first_name)).exists():
            return Response(
                {
                    "status": status.HTTP_409_CONFLICT,
                    "message": "First Name/last Name already exist",
                }
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"status": status.HTTP_409_CONFLICT, "message": "Email Already Exists"}
            )

        username = f"{first_name}.{last_name}"
        if User.objects.filter(username=username).exists():
            return Response(
                {
                    "status": status.HTTP_409_CONFLICT,
                    "message": "Username Already Exists",
                }
            )

        password = get_user_model().objects.make_random_password()
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "message": str(e)})

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.save()

        user_profile, created = Profile.objects.get_or_create(user=user)
        user_profile.user_type = user_type
        user_profile.phone_number = phone_number
        # user_profile.otp = get_random_number()

        category_instance = Category.objects.get(pk=category)
        user_profile.category = category_instance
        user_profile.save()

        # try:
        #     group_instance = Group.objects.get(id=role)
        # except Group.DoesNotExist:
        #     return Response(
        #         {
        #             "status": status.HTTP_400_BAD_REQUEST,
        #             "message": f"Group {role} does not exist",
        #         }
        #     )

        # group_instance.user_set.add(user)
        # send sms to the user

        # sms_url = (
        #     "https://imis.nictanzania.co.tz/production/communication/sms_send/"
        # )
        # sms_params = {
        #     "recipients": phone_number,
        #     "message": f"Welcome to Intern Performance System, your username is:{username}, and password is:{password}",
        #     "customer_name": "",
        #     "module": "InternMS",
        #     "category": 0,
        # }
        # response = requests.post(url=sms_url, data=sms_params)
        # sms_data = response.json()

        # end send sms to user

        # channel = SMSChannel.from_auth_params(
        #     {
        #         "base_url": settings.BASE_URL,
        #         "api_key": settings.API_KEY,
        #     }
        # )

        # sms_response = channel.send_sms_message(
        #     {
        #         "messages": [
        #             {
        #                 "destinations": [{"to": phone_number}],
        #                 "text": "Hello, from Python SDK!",
        #             }
        #         ]
        #     }
        # )

        # Get delivery reports for the message. It may take a few seconds show the just-sent message.
        # query_parameters = {"limit": 10}
        # delivery_reports = channel.get_outbound_sms_delivery_reports(query_parameters)

        # # See the delivery reports.
        # print(delivery_reports)

        return Response(
            {"status": status.HTTP_201_CREATED, "message": "Successfully Created"}
        )


class UserLoginViewSet(viewsets.GenericViewSet):
    serializer_class = LoginSerializer
    queryset = Profile.objects.filter(user__is_active=True)

    @action(detail=False, methods=["POST"])
    def login(self, request):
        phone_number = request.data.get("phone_number")
        otp = None

        if phone_number:
            profile = Profile.objects.filter(
                is_active=True, is_deleted=False, phone_number__iexact=phone_number
            ).first()

            if profile is not None:
                profile.otp = get_random_number()
                otp = profile.otp
                profile.otp_created_at = timezone.now()
                profile.save()

                return Response(
                    {"status": status.HTTP_200_OK, "message": "success", "otp": otp}
                )

            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "No Profile found",
                }
            )

        return Response(
            {"status": status.HTTP_400_BAD_REQUEST, "message": "No User Found"}
        )


class UserVerificationViewSet(viewsets.GenericViewSet):
    serializer_class = LoginSerializer
    queryset = Profile.objects.filter(user__is_active=True)

    @action(detail=False, methods=["POST"])
    def verification(self, request):
        phone_number = request.data.get("phone_number")
        otp = request.data.get("otp")

        if phone_number and otp:
            profile = Profile.objects.filter(
                phone_number__iexact=phone_number, otp__iexact=otp
            ).first()

            if (
                profile
                and profile.user is not None
                and profile.otp_created_at is not None
            ):
                expiration_time = profile.otp_created_at + timedelta(minutes=4)
                current_time = timezone.now()

                if current_time <= expiration_time:
                    user = profile.user
                    # token, created = Token.objects.get_or_create(user=user)
                    token, created = RefreshToken.for_user(user), True
                    serializer = LoginSerializer(user, many=False)
                    return Response(
                        {
                            "status": status.HTTP_200_OK,
                            "message": "OTP Verified successfully",
                            "data": serializer.data,
                            "token": str(token.access_token),
                            "refresh_token": str(token),
                            "expires_at": str(token.access_token.lifetime),
                        }
                    )

                else:
                    return Response(
                        {
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "OTP has Expired",
                        }
                    )

            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Failed to verify OTP",
                }
            )
        return Response(
            {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "Wrong inputs"}
        )


class RegenerateTokenViewSet(viewsets.GenericViewSet):
    serializer_class = LoginSerializer
    queryset = Profile.objects.filter(user__is_active=True)

    @action(detail=False, methods=["POST"])
    def regenerate_otp(self, request):
        phone_number = request.data.get("phone_number")

        if phone_number:
            profile = Profile.objects.filter(
                user__is_active=True,
                is_deleted=False,
                phone_number__iexact=phone_number,
            ).first()

            if profile is not None:
                profile.otp = get_random_number()
                profile.otp_created_at = timezone.now()
                profile.save()

                return Response(
                    {
                        "status": status.HTTP_200_OK,
                        "message": "New OTP requested successfully",
                        "otp": profile.otp,
                    }
                )
            else:
                return Response(
                    {
                        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "message": "No Profile found",
                    }
                )

        return Response(
            {"status": status.HTTP_400_BAD_REQUEST, "message": "No User Found"}
        )


class CategoriesListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.filter(is_active=True, is_deleted=False).order_by(
            "name"
        )

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
