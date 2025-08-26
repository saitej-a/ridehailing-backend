from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .utils import create_response, send_mail_worker
from django.core.cache import cache
from random import randint
from .utils import verifyFirebaseToken
User=get_user_model()


@api_view(['POST'])
def loginUser(request):
    """
    loginUser view:
        - Expects POST request with 'email' in request data.
        - Retrieves the user by email and generates a JWT access token for the user.
        - Returns the access token and user ID in the response.
        - Returns HTTP 200 OK on success.
    """

    user=User.objects.get(email=request.data.get('email',''))
    token=RefreshToken.for_user(user)
    return Response({'access_token':str(token.access_token),'user':user.id},status=status.HTTP_200_OK)



@api_view(['POST'])
def registerUser(request):
    """
    registerUser view:
        - Expects POST request with 'email', 'password', 'phone_number', and 'full_name' in request data.
        - Checks if all fields are provided and if the email or phone number already exists.
        - Checks if both the email and phone number are verified (via OTP or SMS verification in cache).
        - If both are verified, creates a new user with 'is_email_verified' and 'is_phone_verified' set to True.
        - Deletes the verification flags from cache after successful registration.
        - Returns user data with HTTP 201 CREATED on success.
        - If not verified, returns an error message indicating which verification is missing.
    """
    email=request.data.get('email')
    password=request.data.get('password')
    phone_number=request.data.get("phone_number")
    full_name=request.data.get("full_name")
    is_email_verified=cache.get(f'verified_{email}', False)  # Check if the user is verified
    is_phone_verified=cache.get(f'verified_{phone_number}', False)  # Check if the user is verified
    print(is_email_verified, is_phone_verified)
    if not email or not password or not phone_number or not full_name:
        return create_response(False,{"message":"All fields are required"},status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return create_response(False,{"message":"Email Already Exists"},status=status.HTTP_302_FOUND)
    if User.objects.filter(phone_number=phone_number).exists():
        return create_response(False,{"message":"Phone number already exists"})
    
    data={
        "email":email,
        "password":password,
        "full_name":full_name,
        "phone_number":phone_number,

    }
    # print(is_email_verified)
    if is_email_verified and is_phone_verified:
        try:
            data['is_email_verified']=True
            data['is_phone_verified']=True
            user=User.objects.create(**data)
        except Exception as e:
            return create_response(False,{"message":"Failed to create user"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        user_data=CustomUserModelSerializer(user)
        cache.delete(f'verified_{email}')
        cache.delete(f'verified_{phone_number}')
        return create_response(True,{"message":"successfully registered","user":user_data.data},status=status.HTTP_201_CREATED)
    elif not is_email_verified:
        return create_response(False,{"message":"User email not verified"},status=status.HTTP_400_BAD_REQUEST)
    else:
        return create_response(False,{"message":"User phone number not verified"},status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def generateOTP(request):
    """
generateOTP view:
    - Expects POST request with 'email' in request data.
    - Generates a 6-digit OTP and stores it in cache for 1 hour.
    - Sends the OTP to the user's email asynchronously using a background worker.
    - Returns success or failure message based on email sending status.
"""
    email=request.data.get('email')
    otp=randint(100000,999999)
    # print(f'otp_{email}',otp)
    cache.set(f'otp_{email}',otp,3600)
    try:
        send_mail_worker.delay("OTP",f"Your OTP is {otp}",[email])
    except Exception as e:
        return create_response(False,{"message":"Failed to send OTP"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return create_response(True,{"message":"Successfully Otp Sent"},status=status.HTTP_200_OK)



@api_view(['POST'])
def verifyOTP(request):
    """
verifyOTP view:
    - Expects POST request with 'email' and 'otp' in request data.
    - Retrieves the cached OTP for the email and compares it with the provided OTP.
    - If valid, deletes the OTP from cache and sets a verification flag for the user for 1 hour.
    - Returns success or error message based on verification result.
"""
    email=request.data.get('email')
    otp=request.data.get('otp')
    cached_otp=cache.get(f'otp_{email}','')
    print(f'cached_otp: {cached_otp}, otp: {otp}')
    if not cached_otp:
        return create_response(False,{"message":"OTP expired or not found"},status=status.HTTP_400_BAD_REQUEST)
    if str(cached_otp) != str(otp):
        return create_response(False,{"message":"Invalid OTP"},status=status.HTTP_400_BAD_REQUEST)
    
    cache.delete(f'otp_{email}')
    cache.set(f'verified_{email}', True, 3600)  # Store verification status for 1 hour
    return create_response(True,{"message":"OTP verified successfully"},status=status.HTTP_200_OK)

@api_view(['POST'])
def verifySMSOtp(request):
    """
    request needs firebase token
    """
    token = request.data.get("token",None)
    
    if not token:
        return create_response(False, {"message": "Firebase token is required"}, status=status.HTTP_400_BAD_REQUEST)
    results = verifyFirebaseToken(token)
    if not results.get("success"):
        return create_response(False, {"message": "Invalid Firebase token"}, status=status.HTTP_400_BAD_REQUEST)
    phone_number = results['data'].get("phone_number")
    if phone_number and User.objects.filter(phone_number=phone_number).exists():
        return create_response(False, {"message": "User already exists with this phone number"}, status=status.HTTP_400_BAD_REQUEST)
    cache.set(f'verified_{phone_number}', True, 3600)
    return create_response(True, {"message": "Phone number verified successfully", "phone_number": phone_number}, status=status.HTTP_200_OK)