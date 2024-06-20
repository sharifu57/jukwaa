from django.shortcuts import render
from django.utils.encoding import force_bytes
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
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
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
from base.common import get_random_number, send_otp_email, get_otp_number
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings


class UserRegisterViewSet(viewsets.GenericViewSet):
    serializer_class = RegisterSerializer
    queryset = User.objects.filter(is_active=True)

    @action(detail=False, methods=["POST"])
    def register(self, request):
        print("====request data")
        print(request.data)
        email = request.data.get("email")
        first_name = request.data.get("firstName")
        last_name = request.data.get("lastName")
        user_type = request.data.get("userType")
        category = request.data.get("category")
        phone_number = request.data.get("phoneNumber")
        # is_accepted_term = request.data.get("is_accepted_term")
        password = request.data.get("password")
        

        if not email or not first_name or not last_name:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Email and Names are required",
                }
            )

        # if User.objects.filter(Q(first_name=first_name)).exists():
        #     return Response(
        #         {
        #             "status": status.HTTP_409_CONFLICT,
        #             "message": "First Name/last Name already exist",
        #         }
        #     )

        if User.objects.filter(email=email).exists():
            return Response(
                {"status": status.HTTP_409_CONFLICT, "message": "Email Already Exists"}
            )

        base_username = f"{first_name}.{last_name}".lower()
        username = base_username
        num = 1

        while User.objects.filter(username=username).exists():
            username = f"{username}{num}"
            num += 1

        # if User.objects.filter(username=username).exists():
        #     user = User.objects.filter(username=username).first()
        #     user.username = f"{username} + 11"


        # password = get_user_model().objects.make_random_password()
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "message": str(e)})

        
        try:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = False
            user_id = user.id
            # send_otp_email(user_id)
            user.save()
        except Exception as e:
            return Response({'status': 400,'message': f'{e}'})

        user_profile, created = Profile.objects.get_or_create(user=user)
        user_profile.user_type = user_type
        if user_type == 2:
            # trigger an employer profile to make the employer object
            pass

        user_profile.phone_number = phone_number
        user_profile.is_accepted_term = True
        user_profile.otp = get_otp_number()

        category_instance = Category.objects.get(pk=category)
        user_profile.category = category_instance
        token, created = RefreshToken.for_user(user), True
        # access_token = Profile.objects.update(user_access_token=str(token))

        user_profile.user_access_token = str(token)
        user_profile.save()
        serializer = RegisterResponseSerializer(user)

        print("-------testing end end end")
        return Response(
            {"status": status.HTTP_201_CREATED, "message": "Successfully Created", "data": serializer.data}, status.HTTP_201_CREATED
        )


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print("=========start user login")
        print(request.data)
        print("========end user login")
        email_or_username = request.data.get("email", "").strip()
        password = request.data.get("password", "").strip()

        print("=================username and password")
        print(email_or_username)
        print(password)
        print("=================end email and password")

        # Try to fetch the user by email or username
        user = User.objects.filter(Q(email=email_or_username) | Q(username=email_or_username)).first()

        print("=============user")
        print(user)
        print("=============end user")

        if user:
            # Attempt to authenticate the user
            auth_user = authenticate(username=user.username, password=password)

            if auth_user:
                print("=========there is user here")
                refresh = RefreshToken.for_user(user)
                serializer = VerificationSerializer(user)  # Ensure this serializer is correctly implemented

                # Optional: Update last login time
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])

                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "Login Successfully",
                    "data": serializer.data,
                    "token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "expires_at": str(refresh.access_token.lifetime)
                })
            else:
                # If authenticate returns None, it's usually due to a wrong password
                return Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Invalid username or password"
                })
        else:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "User does not exist"
            })


class VerificationViewSet(viewsets.GenericViewSet):
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    @action(detail=False, methods=["POST"])
    def verify(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")


        if not email and not otp:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': "Email and OTP must be provided"})
        
        profile = Profile.objects.filter(user__email__iexact=email, otp=otp).first()

        if not profile:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': "Profile not found or OTP incorrect"})
        
        expiration_time = profile.otp_created_at + timedelta(minutes=4)
        if timezone.now() > expiration_time:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'OTP has expired'})

        user = profile.user
        if user:
            updated_user = User.objects.get(id=user.id)
            updated_user.is_active=True
            print(updated_user.is_active)
            updated_user.save()
        else:
            print("========somthing not fine")

        refresh = RefreshToken.for_user(user)
        profile.user_access_token = str(refresh.access_token)
        profile.save()

        serializer = self.get_serializer(user)

        return Response({
            "status": status.HTTP_200_OK,
            "message": "OTP verified successfully",
            "data": serializer.data,
            "token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "expires_at": str(refresh.access_token.lifetime)
        }, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                # reset_link = reverse(f'$http://localhost:3000/change-password', kwargs={'uidb64': user.pk, 'token': token})
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                # reset_link = f'http://localhost:3000/change-password?token={token}&uidb64={uidb64}'
                reset_link = f'http://{settings.FRONT_END_ADD}/change-password/{token}/{uidb64}'
                # Assume `reset_link` is correctly formed URL to frontend reset page
                send_mail(
                    'Password Reset Request',
                    f'Please go to the following link to reset your password: {request.build_absolute_uri(reset_link)}',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )
                return Response(
                    {
                        'status': status.HTTP_200_OK,
                        'message': 'Password reset link has been sent to your email.'},
                    status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(
                    {'status': status.HTTP_404_NOT_FOUND,
                     'error': 'User with this email does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})


class ResetNewPasswordConfirmAPIView(APIView):
    def post(self, request):
        return
   

class SetNewPasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print("=============my data")
        print(data)
        print("=============end my data")

        serializer = SetNewPasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                print("__________step one")
                uid = urlsafe_base64_decode(serializer.validated_data['uidb64']).decode()
                user = User.objects.get(pk=uid)
                token = serializer.validated_data['token']

                print("_______________token", token)
                print("_________step 2")
                if not default_token_generator.check_token(user, token):
                    return Response({'message': 'Token is invalid or expired', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                # Set the user in serializer context to use in save

                print("=================user id", uid)

                serializer.context['user'] = user
                serializer.save()
                return Response({'message': 'Password has been reset successfully', 'status': status.HTTP_200_OK})
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RegenerateExpiredOTPAPIView(APIView):
    def put(self, request):
        email = request.data.get('email')

        print("========request data")
        print(request.data)
        print("========end request data")
        if email:
            user = User.objects.get(email=email)
            if not user.is_active:
                profile = Profile.objects.filter(user__email__iexact=email).first()

                if profile:
                    try:
                        profile_instance = Profile.objects.get(id=profile.id)
                        profile_instance.otp = get_otp_number()
                        profile_instance.otp_created_at = timezone.now()
                        profile_instance.save()

                        return Response({'status': 200, 'message': 'Successfully generated Otp'})
                    
                    except Profile.DoesNotExist:
                        return Response({
                            'status': 400,
                            'message': 'This user does not Exist'
                        })
                
                else:
                    return Response({
                        'status': 400,
                        'message': 'Profile not found for given email'
                    })
            
            else:
                return Response({
                    'status': 400,
                    'message': "User Already Active, Please Contact administrator"
                })


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


class AllTeamAPIView(APIView):
    def get(self, request):
        teams = Team.objects.filter(is_active=True)
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)


class GetCompaniesLogoAPIView(APIView):
    def get(self, request):
        employers = Employer.objects.filter(is_active=True, is_deleted=False)
        serializer = EmployersLogoSerializer(employers, many=True)
        return Response(serializer.data)


class GetExperienceAPIView(APIView):
    def get(self, request):
        experiences = Experience.objects.filter(is_active=True, is_deleted=False)
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)


class GetUserDetailsAPIView(APIView):
    def get(self, request, user_id=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'No user Available'})

        serializer = RegisterResponseSerializer(user, many=False)
        return Response(serializer.data)


class UpdateUserProfileImageAPIView(APIView):
    def patch(self, request, user_id=None):
        data = request.data
        user_image = data.get('profile_image')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'No User found'})

        profile = Profile.objects.filter(user=user, is_active=True, is_deleted=False).first()

        if profile:
            profile.profile_image = user_image
            profile.save()
            serializer = UserProfileSerializer(profile, many=False)
            return Response({'status': status.HTTP_200_OK, 'message': 'Successfully updated', 'data': serializer.data})

        return Response({'status': status.HTTP_404_NOT_FOUND, 'message': 'No profile found for this user'})


class ForgotPasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        print("-------serialier: %s" % serializer)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            print("=======email is %s" % email)

            if email:
                try:
                    user = User.objects.get(email = email)

                    if user.is_active:
                        profile = Profile.objects.filter(user__email__iexact=email).first()

                        if profile:
                            profile_instance = Profile.objects.get(id=profile.id)
                            my_otp = get_otp_number()
                            profile_instance.password_otp = my_otp
                            profile_instance.password_otp_created_at = timezone.now()
                            profile_instance.save()

                            send_mail(
                                'FORGOT PASSWORD',
                                f'PleasE enter this OTP to proceed to next stage: {my_otp}',
                                'from@example.com',
                                [email],
                                fail_silently=False,
                            )

                            return Response({'status': status.HTTP_200_OK, 'message': 'OTP sent to email'})
                        
                        return Response({'status': status.HTTP_404_NOT_FOUND, 'message': 'Not Found'})
                    return Response({'status': status.HTTP_423_LOCKED, 'message': "User not active"})
                except User.DoesNotExist:
                    return Response({'status': status.HTTP_404_NOT_FOUND, 'message': 'Email not found'})
            return Response({'status': status.HTTP_404_NOT_FOUND, 'message': 'Email not found'})
        return Response({'status': status.HTTP_404_NOT_FOUND, 'message':"Not Valid"})

class VerifyPasswordOTPAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VerifyPasswordOTPSerializer(data=request.data)
        data = request.data
        if data:
            email = data.get('email', None)
            otp = data.get('otp', None)

            if not email and not otp:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Email and OTP must be provided"})

            else:
                profile = Profile.objects.filter(user__email__iexact=email, password_otp=otp).first()
                print(profile)
                if not profile:
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Profile not found or OTP incorrect"})
                
                expiration_time = profile.password_otp_created_at + timedelta(minutes=4)
                if timezone.now() > expiration_time:
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'OTP has expired'})
            
                else:
                    return Response({'status': status.HTTP_202_ACCEPTED, 'message': "Email Successfully Validated"})

        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Data not valid"})