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
from .serializers import *
from django.contrib.auth.models import User
from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
import random
import base64
import json
import jwt

# Create your views here.


def get_random_number():
    otp = random.randint(1000, 9999)
    return otp


def get_random_number():
    projectId = random.randint(1000000,99999999)
    return projectId


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
        is_accepted_term = request.data.get("is_accepted_term")

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
        user_profile.is_accepted_term = True
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

        # end send sms to user

        return Response(
            {"status": status.HTTP_201_CREATED, "message": "Successfully Created"}
        )


class LoginAPIView(APIView):
    def post(self, request, format=None):
        email = request.data.get("email")
        password = request.data.get("password")

        if User.objects.filter(Q(email=email) | Q(username=email)).exists():
            u = User.objects.filter(email=email).first()
            username = u.username
            user = authenticate(username=username, password=password)
            print("user is authenticated")
            print(user)
            if user is not None:
                if user.is_active:
                    # user_serializer = UserSerializer(user, many=False)
                    serializer = VerificationSerializer(user)
                    token, created = RefreshToken.for_user(user), True
                    access_token = Profile.objects.update(user_access_token=str(token))
                    user.last_login = timezone.now()

                    # user_access_token = profile.user_access_token
                    return Response(
                        {
                            "status": status.HTTP_200_OK,
                            "message": "Login Successfully",
                            "data": serializer.data,
                            "token": str(token.access_token),
                            "refresh_token": access_token,
                            "expires_at": str(token.access_token.lifetime),
                        }
                    )
                else:
                    return Response(
                        {
                            "status": status.HTTP_404_NOT_FOUND,
                            "message": "Failed to login (not activated)",
                        }
                    )
            else:
                return Response(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "message": "Invalid username or password",
                    }
                )
        else:
            return Response(
                {"status": status.HTTP_404_NOT_FOUND, "message": "User does not exist"}
            )


class UserMobileLoginViewSet(viewsets.GenericViewSet):
    serializer_class = LoginSerializer
    queryset = Profile.objects.filter(user__is_active=True)

    @action(detail=False, methods=["POST"])
    def user_phone_login(self, request):
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

                sms_url = "https://apiotp.beem.africa/v1/request"
                api_key = settings.OTP_API_KEY  # Replace with your actual API key
                secret_key = (
                    settings.OTP_SECRET_KEY
                )  # Replace with your actual secret key

                auth_str = f"{api_key}:{secret_key}"
                auth_bytes = base64.b64encode(auth_str.encode("utf-8"))
                auth_str_encoded = auth_bytes.decode("utf-8")

                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Basic {auth_str_encoded}",
                }

                sms_params = {"appId": 1, "msisdn": phone_number}
                response = requests.post(url=sms_url, json=sms_params, headers=headers)

                try:
                    sms_data = response.json()
                except ValueError as e:
                    # Handle the case where the response is not valid JSON
                    print(f"Error parsing JSON: {e}")
                    sms_data = {"error": "Invalid JSON response"}

                return Response(
                    {
                        "status": status.HTTP_200_OK,
                        "message": "success",
                        "otp": otp,
                        "phone_number": phone_number,
                        "sms_response": sms_data,
                    }
                )

            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "No Profile found",
                }
            )

        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Phone Number Does not Exist",
            }
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
                    serializer = VerificationSerializer(user, many=False)

                    access_token = Profile.objects.update(user_access_token=str(token))

                    user_access_token = profile.user_access_token
                    return Response(
                        {
                            "status": status.HTTP_200_OK,
                            "message": "OTP Verified successfully",
                            "data": serializer.data,
                            "token": str(token.access_token),
                            "refresh_token": user_access_token,
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


class GetUserAccessTokenAPIView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(
                {"status": status.HTTP_400_BAD_REQUEST, "message": "No User found"}
            )

        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        expires_in_seconds = int(refresh_token.access_token.lifetime.total_seconds())

        data = {
            "refresh_token": str(refresh_token),
            "access_token": access_token,
            "expires_at": expires_in_seconds,
        }

        serializer = RefreshTokenSerializer(data)
        return Response(serializer.data)


class RegenerateTokenViewSet(viewsets.GenericViewSet):
    serializer_class = LoginSerializer
    queryset = Profile.objects.filter(user__is_active=True)

    @action(detail=False, methods=["POST"])
    def regenerate_otp(self, request):
        data = request.data
        if not isinstance(data, dict):
            data = {"phone_number": str(data)}

        phone_number = data.get("phone_number")

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
                        "message": "New OTP Has Been sent",
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


class SkillsListAPIView(APIView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"status": 400, "message": "No Category"})

        skills = Skill.objects.filter(
            category=category, is_active=True, is_deleted=False
        )

        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)


class GetLocationsAPiView(APIView):
    def get(self, request):
        locations = Location.objects.filter(is_active=True, is_deleted=False)
        serializer = LocationSerializer(locations, many=True)

        if locations:
            return Response({'status': 200, 'message': "success", "data": serializer.data})

        else:
            return Response({'status': 400, 'message': "No locations"})


class GetAllUsersAPIView(APIView):
    def get(self, request):
        users = User.objects.filter(is_active=True).order_by('-last_login')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
