import string
import random
import bcrypt
import requests
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
from django.http import HttpResponse
from datetime import timedelta,datetime,timezone
from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .models import user, Role,Company_Users,Plan
from .serializers import (UsersSerializer, UserLimitedSerializer, SignInSerializer, LoginSerializer, RoleSerializer,
                          PermissionsSerializer, GroupSerializer,Company_UsersSeializer)
from django.contrib.auth import authenticate
from registration import Activation_Email
from company.models import Company
from .Activation_Email import send_forgot_password_link
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from registration.serializers import *
from django.db import transaction

import base64
import json
from rest_framework.response import Response
from rest_framework import viewsets


from dotenv import load_dotenv
import os
from Crypto.Cipher import AES
import base64
import json
load_dotenv()
key_b64 = os.getenv("AES_KEY")
iv_b64  = os.getenv("AES_IV")
if not key_b64 or not iv_b64:
    raise Exception("AES_KEY or AES_IV not found")
AES_KEY = base64.b64decode(key_b64)
AES_IV  = base64.b64decode(iv_b64)

# function for validate email
# this function is used to call whether the email is already exist or not
# checking the validate email
def ValidateEmail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if user.objects.filter(email=email).exists():
            messages.warning(request, "email is already exist")
            return redirect('register')
        else:
            if email.is_valid():
                email.save()
                messages.success(request, "user has been registered successfully")
                return redirect('email')
            else:
                messages.error(request, 'Please correct the error.')
    else:
        email = user(request.user)




# this function generate random code 
# for activation code # when you register you will get an activation code through this code you can activate
# your account
def create_random_code(length=8):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

# this function generate random code 
# for password reset # when click on forgot password a random code will be generated 
# and this code is send to your email for validate the user
def create_forgot_password_code(length=8):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


# code for making an sent email for forgot password link
def send_forgetpassword_mail(request, username, pass_code):
    subject = "Your forget password link"
    msg = "Hi , click on the link to reset your password https://products.coderize.in:9003/users/forgetpassword/"
    server_address = f"{request.scheme}://{request.get_host()}/users/User/{username}/ValidateForgotPassword/{pass_code}/"
    recipient_list = [username]
    return True


# View for forget password
@api_view(['GET'])
def forgotpassword(request, email):
    # get an user object and match forgot password code to the pass code
    msg = None
    try:
        user_obj = user.objects.get(email=email)

    except user.DoesNotExist:
        msg = "No user found with this username."
    except Exception as e:
        msg = "error"
    else:
        # pass_code = create_forgot_password_code()
        pass_code = create_forgot_password_code()
        # forgot_pass_code=pass_code
        user_obj.forgot_pass_code = pass_code
        user_obj.forgot_password_is_active = True

        user_obj.forgot_pass_time = datetime.now()

        user_obj.save()

        msg = " An email is sent"
        link_with_code = f"{request.scheme}://{request.get_host()}/registration/User/{user_obj.username}/ValidateForgotPassword/{pass_code}/"

        send_forgot_password_link(user_obj.username, link_with_code)
    return Response({"msg": msg})


# generating a hash password
def create_hashed_password(password):
    # password = b"SuperSercet34"

    # Encode password into a readable utf-8 byte code:
    password = password.encode('utf-8')

    # Hash the ecoded password and generate a salt: 
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    return hashed.decode('UTF-8')
    # if bcrypt.checkpw(password, hashed):
    #     print("Password match!")
    # # Log the user in ...
    # else:
    #     print("Password didn't match")
    #     ("Invalid credentials", "warning")      

class RequestCallView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self,request):
        serializer = RequestCallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(status=201)
        return Response(status=400)

class UserViewset(viewsets.ModelViewSet):
    queryset = user.objects.all()
    serializer_class = UsersSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        raw_data = request.data
        if isinstance(raw_data, str):
            try:
                user_data = decrypt_payload(raw_data)
            except Exception as e:
                return Response({"message": "Invalid payload", "error": str(e)}, status=400)
        else:
            user_data = raw_data
        print("@@@@@@@", user_data)
        n_data = None
        try:
            user.objects.get(email=user_data["email"])
            print("##########", user)
            msg = "Email is already exist"
            print("KKKKKKK", msg)
            return Response({"message":msg},status=status.HTTP_403_FORBIDDEN)
        except user.DoesNotExist:
            try:
                user.objects.get(mobile_no=user_data["mobile_no"])
                print("##########", user)
                msg = "Mobile no is already exist"
                print("KKKKKKK", msg)
                return Response({"message": msg}, status=status.HTTP_403_FORBIDDEN)
            except user.DoesNotExist:

                create_user = user(
                    name=user_data["name"],
                    mobile_no=user_data["mobile_no"],
                    email=user_data["email"],
                    password=create_hashed_password(user_data["password"]),
                    activation_code=create_random_code(),
                    #       forgot_pass_code=UserViewset.forgot_pass_code,
                    is_activated=False,
                    is_subscribed=user_data["is_subscribed"],
                    is_activate=user_data["is_activate"],
                    is_on_trial=True,
                    company=user_data["company"],
                    industry=user_data["industry"],
                    country=user_data["country"],
                    #   username=user_data["email"],
                    username=user_data["email"],
                    department=user_data["department"],
                    image=user_data["image"],
                    provider=user_data["provider"],
                )
                create_user.save()
                token,created  = Token.objects.get_or_create(user=create_user)
                create_user.sub_users.add(create_user)

                activation_link = f"{request.scheme}://{request.get_host()}/registration/activateuser/{create_user.activation_code}"
                Activation_Email.send_activation_email(create_user.name, create_user.email, activation_link)
                print(create_user.email)
                msg = "Congratulation!! Your registration is Successful! Activation link has been sent on your email. Please activate your account."
            
                serializer = UsersSerializer(create_user)
                n_data = serializer.data
                # 14 days time peroid for login 

                # return Response(HTTP_200_OK)
        return Response({"msg": msg, "data": n_data})

        # after the successfull insert please use the send email function


# def sendActivationEmail():
#    # activation_link=f"https://products.coderize.in:9003/users/activateuser/{UserViewset.activation_code}"
#    # Activation_Email.send_activation_email(UserViewset.name, UserViewset.email, activation_link)
#     activation_link=f"https://products.coderize.in:9003/users/activateuser/{UserViewset.activation_code}"
#     Activation_Email.send_activation_email(UserViewset.name, UserViewset.email, activation_link)

# def sendActivationEmail():
#     activation_link = "https://www.auto-counts.com/users/activateuser"
#     Activation_Email.send_email(
#         UserViewset.user1, UserViewset.user_email, activation_link, UserViewset.activation_code)


@api_view(['GET'])
def activateuser(request, act_code):
    try:
        SelectedRecord = user.objects.get(activation_code=act_code)
    except user.DoesNotExist:
        message = "Invalid URL"
    else:
        if SelectedRecord.is_activated is False:
            SelectedRecord.is_activated = True
            SelectedRecord.save()
            message = f"Hi {SelectedRecord.name.title()}. Your account is successfully activated."
        else:
            message = f"Hi {SelectedRecord.name.title()}. Your account is already activated."

    return render(request, "activate_user_response.html", context={"message": message})


def decrypt_payload(payload_b64):
    # 1. Base64 decode
    print("called")
    encrypted_bytes = base64.b64decode(payload_b64)

    # 2. AES decrypt
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    decrypted = cipher.decrypt(encrypted_bytes)

    # 3. Remove PKCS7 padding
    pad_len = decrypted[-1]
    decrypted = decrypted[:-pad_len]

    # 4. Convert bytes to dict
    return json.loads(decrypted.decode("utf-8"))

# post for sign in
# token=Token
# used viewset for get method is not allowed
class signinViewset(viewsets.ViewSet):

    def create(self, request):
        raw_data  = request.data
        print("RAW:", raw_data, type(raw_data))
        if isinstance(raw_data, str):
            try:
                user_data = decrypt_payload(raw_data)  # decrypt AES payload
            except Exception as e:
                return Response({"message": "Invalid payload", "error": str(e)}, status=400)
        else:
            user_data = raw_data

        print("PARSED user_data:", user_data)
        print("API IS HEATING")
        print(f"user_data type: {type(user_data)}")
        print(f"user_data content: {user_data}")
        response_data = {"message": "",
                         #'Token': None,
                         "user_id": None,
                         "data":None}
        print(user_data)
        try:
            # Get a user by its email
            response_data['message'] = "Please check your password."
            Record = user.objects.get(email=user_data["email"])
        except user.DoesNotExist :
            # print(e)
            # Return response if user doesn't exists
            response_data['message'] = "User doesn't exists."
        else:
            # If user is found, check if it is activated
            if Record.is_activated is False:
                # If not activated, send this message
                response_data[
                    'message'] = "Oops! It seems The UserID is not yet activated. Please check the activation link that has been sent on your email!"
            else:
                # If activated, compare its password to see if it is a valid password
                print("REACHED HERE")
                input_password = user_data['password']

                password_in_db = Record.password

                # Check both plane and encrypted password
                if input_password == password_in_db or bcrypt.checkpw(input_password.encode('UTF-8'),
                                                                      password_in_db.encode('UTF-8')):
                    
                    
                    current_date = datetime.now(timezone.utc)#.strptime()).replace(".", "-")
                    print("CURRENT DATE IS",current_date)

                    registration_date=Record.registration_date #.strptime("2026/11/24 09:30", "%Y/%m/%d %H:%M")
                    
                    print("REGISTRATION  DATE EQUAL TO ",registration_date)
                    Enddate =timedelta(days=14)
                    
                    print(" END DATE EQUAL TO ",Enddate)
                    print("DIFFERENTS BEETWEEN TWO DAYS",current_date-registration_date)
                    print("RECORD TRUE OR FALSE",Record.is_activate)
                    if Record.is_activate is True and current_date-registration_date > Enddate :  
                        
                        print("THIS CONDITION IS NOT SATISFIED")
                        print(" REGISTRATION DATE EQUAL TO ",registration_date)
                        print(" END DATE EQUAL TO ",Enddate)
                        Record.is_activate=False
                        print(" RECORD.IS_ACTIVATED STATUUS",Record.is_activate)
                        Record.save()
                        response_data['message']='Your account has expired'
                        return Response(response_data)
                            
                    
               
                      
                    # If password is valid, then send login successful response
                    response_data['message'] = "Login Successful"
                    response_data['data'] = user_data["email"]
                    print()
                    example=UserLimitedSerializer()
                    example.user=Record.id
                            # global token
                    token, _ = Token.objects.get_or_create(user=Record)
                    response_data['token'] = str(token.key)
                    response_data['user_id'] = example.user
                    response_data['access'] = None
                    response_data['role'] = Record.role
                    try:
                        response_data['access'] = UserAccessSerializer(Record.user_access.all()[0]).data
                    except:
                        pass
                else:
                        # If password is not valid, then send this response
                            response_data['message'] = "Please check your password."
                
                

        return Response(response_data)

    

# Get user
global msg


@api_view(['GET'])
def signin(self, useremail, password):
    print(useremail, password)

    Record = user.objects.get(email=useremail, password=password)
    print("record", Record)

    if Record is not None:
        print("record exist")
        # check if user is active
        if Record.is_activated == 'True':
            msg = "user is active"
            print(msg)

        else:
            msg = "user is not active"
            print(msg)
        # check if users password is correct
        if Record.password == password:
            print("access allow", Record.password)
        else:
            print("invalid password")
    else:
        print("not a valid email id")
    serializer = SignInSerializer(Record)
    return Response(serializer.data)


# get all user list
class userList(generics.ListAPIView):
    queryset = user.objects.all()
    serializer_class = UsersSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

# user update by id
@api_view(['PUT'])
def userupdate(request, pk):
    users = user.objects.get(user_id=pk)
    serializer = UsersSerializer(instance=users, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


     
class Logout(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        django_logout(request)
        print("logout successfully")
        return Response()


# API For get all permissions
n_data = None


@api_view(('GET',))
def get_all_permissions(request, obj=None):
    # Individual permissions
    permissions = Permission.objects.all()
    for p in permissions:
        print(p)
    print("permissions", permissions)
    serializer = PermissionsSerializer(permissions, many=True)
    print("serializer################################", serializer.data)
    return Response(serializer.data)


# API for create permissions
class permissionsViewset(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionsSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def create(self, request, *args, **kwargs):
        permissions_data = request.data

        create_permissions = Permission(
            name=permissions_data["name"],
            codename=permissions_data['codename'],
            content_type=ContentType.objects.get_for_model(Permission))
        create_permissions.save()

        serializer = PermissionsSerializer(create_permissions)
        return Response(serializer.data)


# API For get all group
@api_view(('GET',))
def get_all_groups(request, obj=None):
    # Individual permissions
    group = Group.objects.all()
    for g in group:
        print(g)
    print("group", group)
    serializer = GroupSerializer(group, many=True)
    print("serializer################################", serializer.data)
    return Response(serializer.data)


# API for create group view set
class GroupViewset(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def create(self, request, *args, **kwargs):
        groups_data = request.data

        Permission_list = []
        for permissions in groups_data['permissions']:
            permissions = Permission.objects.get(id=permissions)
            print("permissions", permissions)
            Permission_list.append(permissions)
            print("Permission_list", Permission_list)

        create_group = Group(
            name=groups_data["name"], )
        create_group.save()
        create_group.permissions.add(*Permission_list)
        serializer = GroupSerializer(create_group)
        return Response(serializer.data)


# API for role view
class RoleViewset(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def create(self, request, *args, **kwargs):
        role_data = request.data

        create_role = Role(
            name=role_data["name"]
        )

        create_role.save()

        serializer = RoleSerializer(create_role)
        return Response(serializer.data)


class User1Viewset(viewsets.ModelViewSet):
    queryset = user.objects.all()
    serializer_class = UsersSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def create(self, request, *args, **kwargs):
        user_data = request.data

        Permission_list = []
        for user_permissions in user_data['user_permissions']:
            user_permissions = Permission.objects.get(id=user_permissions)
            print("permissions", user_permissions)
            Permission_list.append(user_permissions)
            print("Permission_list", Permission_list)

        role = Role.objects.get(name=user_data["role"])
        create_user = user(
            name=user_data["name"],
            mobile_no=user_data["mobile_no"],
            email=user_data["email"],
            password=user_data["password"],
            image=user_data["image"],
            is_activated=False,
            role=role,
            #        is_subscribed=user_data["is_subscribed"],
            is_activate=user_data["is_activate"],
            is_on_trial=True, )

        create_user.save()
        create_user.user_permissions.add(*Permission_list)

        serializer = UsersSerializer(create_user)
        return Response(serializer.data)



class Company_UsersViewset(viewsets.ModelViewSet):
    queryset = Company_Users.objects.all()
    serializer_class = Company_UsersSeializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def create(self, request, *args, **kwargs):
        companyuser_data = request.data

        User=user.objects.get(pk=companyuser_data["user_id"]),
        company=Company.objects.get(pk=companyuser_data["company_id"]),
        role=Role.objects.get(pk=companyuser_data["role"])

        serializer = Company_UsersSeializer(data=request.data)
        if serializer.is_valid():
            serializer.save
        return Response(serializer.data)


@api_view(['GET'])
def getcompanyusersbyuser_id(request, id):
    queryset = Company_Users.objects.filter(User_id=id)
    serializer = Company_UsersSeializer(queryset, many=True)
    return Response(serializer.data)


class VerifyView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request):
        access = None
        try:
            access = UserAccessSerializer(request.user.user_access.all()[0]).data
        except:
            pass
        return Response({"access":access,"role":request.user.role},status=status.HTTP_200_OK)





class PlanView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        plans = Plan.objects.filter(price__gt=0,user__isnull=True)
        serializer = PlanSerializer(plans,many=True)
        return Response(serializer.data,status=200)