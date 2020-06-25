from django.contrib.auth import get_user_model
from rest_framework import status,permissions
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from knox.views import LoginView as KnoxLogin, LogoutView as KnoxLogout
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.settings import knox_settings
from datetime import *
from BebrasBackend.pagination import *
from BebrasBackend.constants import *
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from com.models import *
from com.serializers import *
from django.db.models import Q
from .password_encryption import encrypt,decrypt

User = get_user_model()

class LoginView(KnoxLogin):                        #Login ApI for Admin and Author
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user!= None:
            update_last_login(None, user)
            s = UserSerializer(user).data['userID']
            s1 = (UserRole.objects.filter(userID=s)).values('RoleID')
            approved = code.objects.get(codeID=user.is_active.codeID)
            if approved.codeName=="approved" and s1:
                s2=s1[0]['RoleID']
                if (s2==1 or s2==4):
                    return Response({
                        "user": UserSerializer(user).data,
                        "token": AuthToken.objects.create(user)[1],
                        "expiry" : knox_settings.TOKEN_TTL
                    })
                else:
                    return Response("User is not an Admin")
            else:
                return Response("User is not an Admin")
        else:
            return Response("Invalid User")


class LogoutView(KnoxLogout):                        #Logout API for Admin and Author
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        request._auth.delete()
        return Response(status=204)


class UpdateView(APIView):                          #User Details- Update API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request,**kwargs):
         id = UserRole.objects.get(userRoleID = kwargs['userRoleID'])
         serializers = UserRoleInsertUpdateSerializer(instance=id, data = request.data,partial=True)
         serializers.is_valid(raise_exception=True)
         serializers.save(modified_on = datetime.now().date() )
         return Response(serializers.data)


class UpdateProfileView(APIView):                 #Update API Admin and Author Profile
     authentication_classes = (TokenAuthentication, )
     permission_classes = (permissions.IsAuthenticated,)

     def post(self,request,**kwargs):
         id = User.objects.get(userID = kwargs['userID'])
         serializers = UserInsertUpdateSerializer(instance=id, data = request.data,partial=True)
         serializers.is_valid(raise_exception=True)
         serializers.save(modified_on = datetime.now().date() )
         return Response(serializers.data)


class UserAdminView(APIView):                   #Get All Admins API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        roleref = Role.objects.get(RoleName='Admin')
        employee1 = UserRole.objects.filter(RoleID=roleref.RoleID)
        serializer = UserRoleSerializer(employee1,many=True)
        return Response(serializer.data)


class SingleUserProfile(APIView):                   #Get Details of Single User API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,**kwargs):
        employee1 = User.objects.filter(loginID = kwargs['loginID'])
        serializer = UserSerializer(employee1,many=True)
        return Response(serializer.data)


class UserPageView(APIView):                       #Get All Users API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        queryset = UserRole.objects.all()
        paginator = CustomPagination()
        response = paginator.generate_response(queryset,UserRoleSerializer,request)
        return Response(response.data)

class GetUsersYearWise(APIView):                       #Get YearWise Users API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,**kwargs):
        users = User.objects.filter(created_on__icontains = kwargs['year']).values_list('userID', flat=True)
        usersIDlist = list(users)
        queryset = UserRole.objects.filter(userID__in = usersIDlist)
        paginator = CustomPagination()
        response = paginator.generate_response(queryset,UserRoleSerializer,request)
        return Response(response.data)

class InsertUserView(APIView):          #Insert New Admin and Author API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def SendMail(self,request):
        subject_template_name = 'New User @Bebras Admin';
        fromaddr = "softcornercummins@gmail.com"
        toaddr = request.data['userID']['loginID']
        mail = MIMEMultipart()
        mail['From'] = fromaddr
        mail['To'] = toaddr
        mail['Subject'] = subject_template_name
        body = "Hello, " + request.data['userID']['username'] + \
            "\n\nYou're receiving this email because you have been appointed as a/an "+request.data['RoleID']['RoleName']+" at Bebras Admin.\n\n" + \
               "You can go visit the website now: \n" + \
                baseURL+"#/login" + \
               "\n\nYour credentials are:\nUsername: " + request.data['userID']['loginID'] + \
                "\nPassword: " + request.data['userID']['password'] + \
                "\n\n Thank you and Regards," + \
                "\n\n\nThe Bebras Admin team"
        mail.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, 'softcorner@2020')
        text = mail.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

    def post(self, request):
        serializer = UserRoleInsertUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.SendMail(request)
        return Response(status = status.HTTP_200_OK)

class ResetPasswordView(APIView):          #API for Reset Password

    def reset_password(self, user, request):
        c = {
            'email': user.email,
            'domain': request.META['HTTP_HOST'],
            'site_name': 'Bebras Admin',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
        }
        subject_template_name = 'Password Reset';
        fromaddr = "softcornercummins@gmail.com"
        toaddr = user.loginID
        mail = MIMEMultipart()
        mail['From'] = fromaddr
        mail['To'] = toaddr
        mail['Subject'] = subject_template_name
        body = "You're receiving this email because you requested a password reset for your user account at " + c['site_name'] + ".\n\n" + \
               "Please go to the following page and choose a new password: \n" + \
                baseURL+"#/resetPassword/?uidb64="+c['uid'] + "&token=" + c['token'] + \
               "\n\n\nYour username, in case you've forgotten: " + c['email'] + \
                "\n\nThanks for using our site!" + \
                "\n\n\nThe " + c['site_name'] + " team"
        mail.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, 'softcorner@2020')
        text = mail.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

    def post(self, request, *args, **kwargs):
        associated_users = User.objects.filter(loginID=request.data['emailID'])
        if associated_users.exists():
            for user in associated_users:
                self.reset_password(user, request)
            return Response("Email sent to the registered email id")
        else:
            return Response("Error")

class ConfirmResetPasswordView(APIView):                     #API for Connfirm Password

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        UserModel = get_user_model()
        assert uidb64 is not None and token is not None
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            id = User.objects.get(loginID=user)
            serializers = PasswordResetSerializer(id, data=request.data, partial=True)
            serializers.is_valid(raise_exception=True)
            saved = serializers.save(modified_on=datetime.now().date())
            if saved:
                return Response(status=200)
            else:
                return Response(status=501)
        else:
            return Response(status=410)

class RoleListView(APIView):                 #Get All Roles API
     authentication_classes = (TokenAuthentication, )
     permission_classes = (permissions.IsAuthenticated,)

     def get(self,request):
        employee1 = Role.objects.all()
        serializer = RoleInsertUpdateSerializer(employee1,many=True)
        return Response(serializer.data)

class RoleListAdd(APIView):                    #Get All Roles for Insert User API
     authentication_classes = (TokenAuthentication, )
     permission_classes = (permissions.IsAuthenticated,)

     def get(self,request):
        list = ['Admin','Author']
        employee1 = Role.objects.filter(RoleName__in=list)
        serializer = RoleInsertUpdateSerializer(employee1,many=True)
        return Response(serializer.data)

class ChangePasswordView(APIView):              #API for Change Password
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
         serializer = PasswordChangeSerializer(data=request.data)
         user = User.objects.get(loginID = request.data['loginID'])
         if serializer.is_valid():
            if not decrypt(user.password)==serializer.data.get('old_password'):
                return Response({'old_password': ['Wrong password.']},
                                status=status.HTTP_400_BAD_REQUEST)
            user.password = encrypt(serializer.data.get('new_password'))
            user.modified_on = datetime.now().date()
            user.modified_by = request.data['loginID']
            user.save()
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)
         return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class GetGenderView(APIView):                #Get All Gender API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        gender = codeGroup.objects.get(codeGroupName='gender')
        gendertypes = code.objects.filter(codeGroupID=gender.codeGroupID)
        serializer = CodeSerializer(gendertypes,many=True)
        return Response(serializer.data)


class UserPTimeline(APIView):             #Get Single User Timeline API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, **kwargs):
        usrdata=User.objects.filter(Q(created_by__startswith=kwargs['loginID']) | Q(modified_by__startswith=kwargs['loginID']))
        serializer = UserSerializer(usrdata,many=True)
        return Response(serializer.data)


class GetUserRoleLocationPageView(APIView):            #View All users according to type API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,**kwargs):
        type=kwargs['type']
        if(type=='school'):
            locationType=code.objects.get(codeName='schoolID')
            list=UserRoleLocation.objects.filter(locationObjectID=kwargs['schoolID'],locationTypeCodeID=locationType)
            paginator = CustomPagination()

        elif(type=='state'):
            locationType = code.objects.get(codeName='stateID')
            list = UserRoleLocation.objects.filter(locationObjectID=kwargs['stateID'],
                                                       locationTypeCodeID=locationType)
            paginator = CustomPagination()

        elif(type=='country'):
            locationType = code.objects.get(codeName='countryID')
            list = UserRoleLocation.objects.filter(locationObjectID=kwargs['countryID'],
                                                       locationTypeCodeID=locationType)
            paginator = CustomPagination()

        response = paginator.generate_response(list,UserRoleLocationSerializer,request)
        return Response(response.data)


class GetUserRoleLocationView(APIView):                    #Get all roles according to type API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,**kwargs):
        type=kwargs['type']
        if(type=='school'):
            locationType=code.objects.get(codeName='schoolID')
            list=UserRoleLocation.objects.filter(locationObjectID=kwargs['schoolID'],locationTypeCodeID=locationType)

        elif(type=='state'):
            locationType = code.objects.get(codeName='stateID')
            list = UserRoleLocation.objects.filter(locationObjectID=kwargs['stateID'],
                                                       locationTypeCodeID=locationType)

        elif(type=='country'):
            locationType = code.objects.get(codeName='countryID')
            list = UserRoleLocation.objects.filter(locationObjectID=kwargs['countryID'],
                                                       locationTypeCodeID=locationType)

        serializers = UserRoleLocationSerializer(list,many=True)
        return Response(serializers.data)


class GetRegisteredBy(APIView):                          #Get Details of teacher Registered School API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,**kwargs):
        lists=User.objects.filter(loginID=kwargs['loginID'])
        serializer= UserSerializer(lists,many=True)
        return Response(serializer.data)

class GetDistinctUserYears(APIView):                          #Get Distinct User Years API
      authentication_classes = (TokenAuthentication, )
      permission_classes = (permissions.IsAuthenticated,)

      def get(self,request):
        lists=User.objects.dates('created_on','year')
        return Response({"data":lists})



