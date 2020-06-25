from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import *
from .models import *
from cmp.models import *
from ques.models import *
from cmp.serializers import *
from com.models import *
from com.serializers import *
from BebrasBackend.constants import *
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import *
import smtplib
from datetime import *
from phonenumber_field.phonenumber import to_python
from email.mime.multipart import MIMEMultipart
from geopy.exc import GeocoderTimedOut
from django.contrib.auth import get_user_model
from email.mime.text import MIMEText
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
import random
import string
import requests
from .password_encryption import encrypt,decrypt
from geopy.geocoders import Nominatim
class LoginAPI(generics.GenericAPIView):
    permission_classes = [
      permissions.AllowAny,
    ]
    serializer_class = LoginSerializer
    def post(self, request,format='json'):
      try:
        print(request.data)
        serializer = LoginSerializer(data=request.data)
        print(request.data['loginID'])
        if serializer.is_valid():
          try:
                user1=User.objects.get(loginID=request.data['loginID'])
                pass_decrypt=decrypt(user1.password)
                print(pass_decrypt)
                if(pass_decrypt==request.data['password']):
                  print("Password and loginID correct: ",user1.loginID)
                  user1.last_login=datetime.now()
                  user1.save()
                  user_role=UserRole.objects.get(userID=user1.userID)
                  role=Role.objects.get(RoleID=user_role.RoleID.RoleID)
                  print("Role of user :",role.RoleName)
                  if(role.RoleID==AdminRoleID):
                        return Response("You seem to be an Admin,Please login using admin portal",status=400)
                  elif(role.RoleID!=AdminRoleID and user1.is_active.codeID==unapproved):
                        return Response("Please login after some time, you are not approved yet...",status=400)
                  elif(role.RoleID!=AdminRoleID and user1.is_active.codeID==active):
                        return Response({

                        "user": UserSerializer(user1, context=self.get_serializer_context()).data,
                        "userrole":role.RoleName,
                        "token": AuthToken.objects.create(user1)[1]
                          })
                  elif(role.RoleName!='admin' and user1.is_active.codeID==inactive):
                        return Response("You aren't active anymore,Please contact admin...",status=400)
                else:
                    return Response("Invalid password",status=400)
          except User.DoesNotExist:
                return Response("User is not Registered",status=400)

        else:
          errors=''
          for i in serializer.errors :
              errors=errors+ i +' '+ str(serializer.errors[i])
              errors="Error : "+errors
          raise_exception=True
          return JsonResponse(errors, status=400)
      except Exception as e:
        return HttpResponse(e,status=500)
class TeacherRegisterAPI(generics.GenericAPIView):

    permission_classes = [permissions.AllowAny,]
    serializer_class = RegisterSerializer

    def post(self, request):
      try:
        print("Recieved a request ",request.data)
        pass_encrypt=encrypt(request.data['password'])
        request.data['password']=pass_encrypt
        Code=code.objects.get(codeName=request.data['gender'])
        school1=school.objects.get(schoolID=request.data['school'])
        request.data['gender']=Code.codeID
        request.data['loginID']=request.data['email']
        del request.data['school']
        print(request.data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
          user = serializer.save()  #if serialzer is valid,save data into myapp_ user table
          if str(user) =="Can't save into database":
            return Response("Can't register user at this moment ,Please Try Again",status=400)
          uid=user.userID
          user=User.objects.get(userID=uid)
          school1.registered_By=user.loginID
          school1.modified_by=user.loginID
          school1.save()
          user.created_by=user.loginID
          user.modified_by=user.loginID
          user.save()
          userroledata['userID']=uid  #userroledata used from constants.py
          userroledata['RoleID']=TeacherRoleID #TeacherRoleID used from constants.py
          print(userroledata)
          roleserializer=AddUserRoleSerializer(data=userroledata) #dump into myapp_userrole table
          if roleserializer.is_valid():
            userroleid=roleserializer.save() # put data into userrole serializer
            print("user role saved")
            userRoleLocationdata["locationObjectID"]=school1.schoolID
            userRoleLocationdata["userRoleID"]=userroleid.userRoleID
            print(userRoleLocationdata)
            roleserializer=AddUserRoleLocationSerializer(data=userRoleLocationdata)
            if roleserializer.is_valid():
              userrolelocationid=roleserializer.save()
              print("Object saved")
              return Response({
            "user": UserViewSerializer(user, context=self.get_serializer_context()).data,
              })
            else:
              return Response("can't save userrole location data",status=404)
          else:
              return Response("can't save userrole  data",status=404)
        else:
          raise_exception=True
          errors=''
          for i in serializer.errors :
              errors=errors+ i +' '+ str(serializer.errors[i])
              errors="Error : "+errors

          return JsonResponse(errors  ,status=400)
      except Exception as e:
        return HttpResponse(e,status=404)
class StudentBulkCompetitionRegisterAPI(generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = RegisterSerializer

    def post(self, request):
      try:
        responsedata=[]
        print("Received a request ",request.data)
        cmpName=request.data['competitionName']
        comp=competition.objects.get(competitionName=cmpName)
        cmpage=competitionAge.objects.filter(competitionID=comp.competitionID)
        print("got competition age ")
        for cmps in cmpage:
          classnumber=int(request.data['classNumber'])
          if cmps.AgeGroupClassID.ClassID.classID==classnumber:
            cmpageID=cmps.competitionAgeID
        lang=request.data['language']
        langcode=code.objects.get(codeName=lang)
        studentEnrollmentdata['competitionAgeID']=cmpageID
        studentEnrollmentdata['languageCodeID']=langcode.codeID
        usrrole=UserRole.objects.get(userID=request.user.userID)
        print(usrrole)
        usrroleLocation=UserRoleLocation.objects.get(userRoleID=usrrole.userRoleID)
        print(usrroleLocation.locationObjectID)
        school_name = school.objects.get(schoolID=usrroleLocation.locationObjectID)
        schclass=schoolClass.objects.get(schoolID=school_name.schoolID,classNumber=request.data['classNumber'])
        studentEnrollmentdata['schoolClassID']=schclass.schoolClassID
        print("going into serializer",studentEnrollmentdata)
        studentdata=request.data['user']
        for data in studentdata:
          user=User.objects.get(loginID=data['loginID'])
          try:
            studentenrolled=studentEnrollment.objects.get(userID=user.userID,competitionAgeID=cmpageID)
            responsedata.append('Already registered '+ user.loginID)
            continue
          except studentEnrollment.DoesNotExist:
            studentEnrollmentdata['userID']=user.userID
            print(studentEnrollmentdata)
            serializer=CmpEnrollmentSerializer(data=studentEnrollmentdata)
            if serializer.is_valid():
              enrolledstudent = serializer.save()
              enrolledstudent=CmpEnrollmentSerializer(enrolledstudent, context=self.get_serializer_context()).data
              responsedata.append(enrolledstudent)
              print("Student registered succesful")
            else:
              return Response("Invalid data",status=400)
            print(responsedata)
        return JsonResponse(responsedata, safe=False,status=200)
      except:
        errors=''
        for i in serializer.errors :
              errors=errors+ i +' '+ str(serializer.errors[i])
              errors="Error : "+errors
        return HttpResponse(errors,status=400)
class StudentRegisterAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = RegisterSerializer
    def loginID_generator(first_name,last_name):
      val = "{0}{1}".format(first_name[0],last_name).lower()
      x=0
      while True:
          if x == 0 and User.objects.filter(loginID=val).count() == 0:
              return val
          else:
              new_val = "{0}{1}".format(val,x)
              print("trying",new_val)
              if User.objects.filter(loginID=new_val).count() == 0:
                return new_val
          x += 1
          if x > 1000000:
              raise Exception("Name is super popular!")

    def password_generator(Firstname,Lastname):
      password_characters ="CSBC"+ string.ascii_letters+  string.digits
      password=random.choice(Firstname[0].upper())
      password=password+random.choice(string.punctuation)
      password=password+random.choice(Lastname.lower())
      password=password+random.choice(string.punctuation)
      newpassword= ''.join(random.choice(password_characters) for i in range(8))
      return password+newpassword

    def post(self, request):
      try:
        print("Received a request ",request.data)
        Firstname=request.data['firstName']
        Lastname=request.data['lastName']
        username=Firstname+" "+Lastname
        Code=code.objects.get(codeName=request.data['gender'])
        request.data['gender']=Code.codeID
        request.data['username']=username
        loginID=StudentRegisterAPI.loginID_generator(Firstname,Lastname)
        request.data['loginID']=loginID
        password=StudentRegisterAPI.password_generator(Firstname,Lastname)
        request.data['password']=password
        pass_encrypt=encrypt(request.data['password'])
        request.data['password']=pass_encrypt
        if request.data['birthdate']=='':
          request.data['birthdate']=None
        if not request.data['email']:
          request.data['email']=None
        if request.data['email']=='':
          request.data['email']=None
        if request.data['phone']=='':
          request.data['phone']=None
        print("Sending to serializer",request.data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
          user = serializer.save()  #if serialzer is valid,save data into myapp_ user table
          if str(user) =="Can't save into database":
            return Response("Can't register user at this moment ,Please Try Again",status=400)
          user=User.objects.get(loginID=loginID)
          userloggedin=User.objects.get(userID=request.user.userID)
          user.created_by=userloggedin.loginID
          user.modified_by=userloggedin.loginID
          codeid=code.objects.get(codeID=active)
          user.is_active=codeid
          user.save()
          print("User saved ")
          userroledata['userID']=user.userID  #userroledata used from constants.py
          userroledata['RoleID']=StudentRoleID #TeacherRoleID used from constants.py
          roleserializer=AddUserRoleSerializer(data=userroledata) #dump into myapp_userrole table
          if roleserializer.is_valid():
            userroleid=roleserializer.save() # put data into userrole serializer
          print("Student saved in userrole table")
          return Response({ "firstName":Firstname,"lastName":Lastname,"username":username,
                            "loginID":loginID,"password":password})
        else:
          errors=''
          for i in serializer.errors :
              errors=errors+ i +' '+ str(serializer.errors[i])
              errors="Error : "+errors
          raise_exception=True
          return JsonResponse(errors, status=400)
      except Exception as e:
        return HttpResponse(e,status=500)

  # StudentBulk  Register API
class StudentBulkRegisterAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = RegisterSerializer
    def post(self, request):

      responsedata=[]
      try:
        for data in request.data:
          #requesting StudentRegister API
          try:
            print(data)
            Firstname=data['firstName']
            Lastname=data['lastName']
            username=Firstname+" "+Lastname
            Code=code.objects.get(codeName=data['gender'])
            data['gender']=Code.codeID
            data['username']=username
            loginID=StudentRegisterAPI.loginID_generator(Firstname,Lastname)
            data['loginID']=loginID
            password=StudentRegisterAPI.password_generator(Firstname,Lastname)
            data['password']=password
            pass_encrypt=encrypt(data['password'])
            data['password']=pass_encrypt
            if data['birthdate']=='':
              data['birthdate']=None
            if not data['email']:
              data['email']=None
            if data['email']=='':
              data['email']=None
            if data['phone']=='':
              data['phone']=None
            print("Sending to serializer",data)
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
              user = serializer.save()  #if serialzer is valid,save data into myapp_ user table
              if str(user) =="Can't save into database":
                return Response("Can't register user at this moment ,Please Try Again",status=400)
              user=User.objects.get(loginID=loginID)
              userloggedin=User.objects.get(userID=request.user.userID)
              user.created_by=userloggedin.loginID
              user.modified_by=userloggedin.loginID
              codeid=code.objects.get(codeID=active)
              user.is_active=codeid
              user.save()
              print("User saved ")
              userroledata['userID']=user.userID  #userroledata used from constants.py
              userroledata['RoleID']=StudentRoleID #TeacherRoleID used from constants.py
              roleserializer=AddUserRoleSerializer(data=userroledata) #dump into myapp_userrole table
              if roleserializer.is_valid():
                userroleid=roleserializer.save() # put data into userrole serializer
              print("Student saved in userrole table")

              responsedata.append({ "firstName":Firstname,"lastName":Lastname,"username":username,
                                "loginID":loginID,"password":password})
            else:
              errors=''
              for i in serializer.errors :
                  errors=errors+ i +' '+ str(serializer.errors[i])
              errors="Didn't register the student because "+errors
              raise_exception=True
              responsedata.append({ "firstName":Firstname,"lastName":Lastname,"username":username,
                                "loginID":loginID,"password":errors})

            return JsonResponse(responsedata, safe=False,status=200)
          except:
            errors=''
            for i in serializer.errors :
                  errors=errors+ i +' '+ str(serializer.errors[i])
            return  HttpResponse(errors,status=400)
      except:
        return HttpResponse("Can't register please try again",status=400)


  #When Teacher Registers Another Teacher
class TeacherRegistrationAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = RegisterSerializer

    def post(self, request):
      try:
        print("Received a request ",request.data)
        pass_encrypt=encrypt(request.data['password'])
        request.data['password']=pass_encrypt
        Code=code.objects.get(codeName=request.data['gender'])
        request.data['gender']=Code.codeID
        request.data['loginID']=request.data['email']
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
          user = serializer.save()  #if serialzer is valid,save data into myapp_ user table
          if str(user) =="Can't save into database":
            return Response("Can't register user at this moment ,Please Try Again",status=400)
          user=User.objects.get(email=request.data['email'])
          userloggedin=User.objects.get(userID=request.user.userID)
          user.created_by=userloggedin.loginID
          user.modified_by=userloggedin.loginID
          codeid=code.objects.get(codeID=active)
          user.is_active=codeid
          user.save()
          print("User saved")
          usr_role=UserRole.objects.get(userID=request.user.userID)
          usr_location=UserRoleLocation.objects.get(userRoleID=usr_role.userRoleID)
          userroledata['userID']=user.userID  #userroledata used from constants.py
          userroledata['RoleID']=TeacherRoleID #TeacherRoleID used from constants.py
          roleserializer=AddUserRoleSerializer(data=userroledata) #dump into myapp_userrole table
          if roleserializer.is_valid():
            userroleid=roleserializer.save() # put data into userrole serializer
            print("User saved in usrrole ")
            userRoleLocationdata["locationObjectID"]=usr_location.locationObjectID
            userRoleLocationdata["userRoleID"]=userroleid.userRoleID
            roleserializer=AddUserRoleLocationSerializer(data=userRoleLocationdata)
            if roleserializer.is_valid():
              userrolelocationid=roleserializer.save()
          print("User saved in userrolelocation")
          return Response({
          "user": UserViewSerializer(user, context=self.get_serializer_context()).data,  })
        else:
          errors=''
          for i in serializer.errors :
              errors=errors+ i +' '+ str(serializer.errors[i])
              errors="Error : "+errors
          raise_exception=True
          return JsonResponse(errors,status=400)
      except Exception as e:
        return HttpResponse(e,status=404)

  # Get All Users Created by a Teacher API
class UserViewAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserViewSerializer

    def get(self, request, format=None):
      try:
        current_user = request.user
        print("Current user ",current_user.userID)
        userroles=UserRole.objects.filter(RoleID=StudentRoleID).values_list('userID', flat=True)
        user_ids=list(userroles)
        users = User.objects.filter(userID__in=user_ids,created_by=current_user.loginID)
        serializer = UserViewSerializer(users, many=True)
        return JsonResponse({"users":serializer.data}, safe=False)
      except Exception as e:
        return HttpResponse(e,status=401)
class UserAPI(generics.RetrieveAPIView):

    permission_classes = [
      permissions.IsAuthenticated,
    ]
    serializer_class = UserViewSerializer
    def get_object(self):
      try:
        return self.request.user
      except Exception as e:
        return HttpResponse(e,status=404)

  # School Register API
class SchoolRegisterAPI(generics.GenericAPIView):
    permission_classes = [
      permissions.AllowAny,
    ]
    serializer_class = AddressSerializer
    def validate_international_phonenumber(value):
      phone_number = to_python(value)
      if  phone_number.is_valid():
        return True
    def post(self, request):
      try:
        print("Recievd a request ",request.data)
        addressdata=request.data['address']
        schooldata=request.data['school']
        cl=schooldata["classes"]
        country=Countries.objects.get(name=addressdata['country'])
        state=States.objects.get(name=addressdata['state'])
        district=Districts.objects.get(name=addressdata['district'],stateID=state.stateID)
        print("school data",schooldata)
        schooldata['phone']=schooldata['contact']
        del schooldata['contact']
        if not SchoolRegisterAPI.validate_international_phonenumber(schooldata['phone']) :
            return Response( "The phone number entered is not valid.",status=400)

        if schooldata['UDISEcode']!='' and len(schooldata['UDISEcode'])!=11:
          return Response("Udisecode should be eleven digits",status=404)
        geolocator = Nominatim(user_agent="bebras")
        try:
          location = geolocator.geocode(schooldata['schoolName']+" "+addressdata['pincode'])
          if location is None:
            print("not found location")
            location = geolocator.geocode(addressdata['pincode'])
            if location is None:
              print("not found pin")
              location = geolocator.geocode(addressdata['city'])
          addressdata['latitude']=location.latitude
          addressdata['longitude']=location.longitude
        except GeocoderTimedOut as e:
          print("Error: geocode timeout on input")
          addressdata['latitude']=28.5669
          addressdata['longitude']=77.2423
        addressdata['districtID']=district.districtID
        addressdata['stateID']=state.stateID
        addressdata['countryID']=country.countryID
        print("address",addressdata)
        serializer = AddAddressSerializer(data=addressdata)
        if serializer.is_valid():
          address = serializer.save()
          typecode=code.objects.get(codeName=schooldata['schoolType'])
          print("address saved")
          schooldata['schoolTypeCodeID']=typecode.codeID
          typecode=code.objects.get(codeName=schooldata['schoolGroupID'])
          schooldata['schoolGroupID']=typecode.codeID
          schooldata['addressID']=address.addressID
          del schooldata['schoolType']
          serializer = AddSchoolSerializer(data=schooldata)
          if serializer.is_valid():
            school1 = serializer.save()
            print("school saved")
            for i in cl:
              schoolclassdata1["schoolID"]=school1.schoolID
              schoolclassdata1["classNumber"]=i
              serializer = AddschoolClassSerializer(data=schoolclassdata1)
              if serializer.is_valid():
                classes = serializer.save()
                print("school class saved")
            return Response({
            "address": AddAddressSerializer(address, context=self.get_serializer_context()).data,
            "school":school1.schoolID,
            "classes":AddschoolClassSerializer(classes, context=self.get_serializer_context()).data,
              })
          else:
            errors=''
            for i in serializer.errors :
              errors=errors+ i +' '+ str(serializer.errors[i])
              errors="Error : "+errors
            raise_exception=True
            return JsonResponse(errors, status=400)
        else:
          raise_exception=True
          errors=''
          for i in serializer.errors :
              errors=errors+ i +' '+ str(serializer.errors[i])
              errors="Error : "+errors
          return JsonResponse(errors, status=400)
      except Exception as exc:
        print(exc)
        return JsonResponse( exc ,status=400)
class UserExcelAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = StudentSerializer

    def get(self, request, format=None):
      try:
        current_user = request.user
        print("User logged in ",current_user.loginID)
        userroles=UserRole.objects.filter(RoleID=StudentRoleID).values_list('userID', flat=True)
        user_ids=list(userroles)
        users = User.objects.filter(userID__in=user_ids,created_by=current_user.loginID)
        serializer = StudentSerializer(users, many=True)
        for data in serializer.data:
          pass_decrypt=decrypt(data['password'])
          data['password']=pass_decrypt
          print(data)
        return JsonResponse({"users":serializer.data}, safe=False)
      except Exception as e:
        return HttpResponse(e,status=401)
class ResetPasswordView(APIView):

    def reset_password(self, user, request):

        global c
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
        print("uid " + c['uid'])
        print('token ' + c['token'])
        fromaddr = "softcornercummins@gmail.com"
        toaddr = user.loginID
        mail = MIMEMultipart()
        mail['From'] = fromaddr
        mail['To'] = toaddr
        mail['Subject'] = subject_template_name
        body = "You're receiving this email because you requested a password reset for your user account at " + c['site_name'] + ".\n\n" + \
               "Please go to the following page and choose a new password:\n" + \
                baseurl+"forgot-password/?uidb64="+c['uid'] + "&token=" + c['token'] + \
               "\n\n\nYour loginID, in case you've forgotten:" + c['email'] + \
                "\n\nThanks for using our site!" + \
                "\n\n\nThe " + c['site_name'] + " team"
        mail.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(fromaddr, 'softcorner@2020')
        text = mail.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

    def post(self, request, *args, **kwargs):
        print((request.data))
        associated_users = User.objects.get(loginID=request.data['loginID'])
        print(associated_users)
        if associated_users:
            userrole=UserRole.objects.get(userID=associated_users.userID)
            print(userrole)
            if userrole.RoleID.RoleID==TeacherRoleID:
                self.reset_password(associated_users, request)
                return JsonResponse({"uidb64":c['uid'],"token":c['token'],"response":"Email sent to the registered email id"})
                return Response("Email sent to the registered email id")
            else:
                return Response("Please contact your respective teacher for login credentials",status=404)
        else:
            return Response("Error User Not Found",status=404)
class ConfirmResetPasswordView(APIView):
    def confirmationEmail(self, user, request):

        global c
        c = {
            'email': user.email,
            'domain': request.META['HTTP_HOST'],
            'site_name': 'Bebras Admin',
            'user': user,
            'protocol': 'http',
        }
        subject_template_name = 'Your password has been changed';
        fromaddr = "softcornercummins@gmail.com"
        toaddr = user.loginID
        mail = MIMEMultipart()
        mail['From'] = fromaddr
        mail['To'] = toaddr
        mail['Subject'] = subject_template_name
        body = "This is a confirmation that the password for your Bebras account \n" + \
        c['email'] + \
        "\nhas just been changed \n" + \
        "If you didn't change your password, you can secure your account by resetting the password again using forgot password at login page.\n"+ \
        "If you're having trouble, please write your query at the contact us section.\n\n\n" + \
        "From\n" + \
        "The Bebras Team"
        mail.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(fromaddr, 'softcorner@2020')
        text = mail.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

    def post(self, request, uidb64='None', token='None', *arg, **kwargs):

        print("Recievd a request ",request.data)
        uidb64=request.data['uidb64']
        token=request.data['token']
        UserModel = get_user_model()
        print(UserModel)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
            print("got user ",user)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        if user is not None:
          print("user found")
        print(default_token_generator.check_token(user, token))
        if user is not None and default_token_generator.check_token(user, token):
            id = User.objects.get(loginID=user.loginID)
            # request.data['password']=encrypt(request.data['password'])
            serializers = PasswordResetSerializer(id, data=request.data, partial=True)
            serializers.is_valid(raise_exception=True)
            saved = serializers.save(modified_on=datetime.now().date())
            if saved:
                self.confirmationEmail(user, request)
                return Response("Password reset Success")
            else:
                return Response('Password reset has not been successful.',status=400)

        else:
            return Response('The reset password link is no longer valid.',status=404)
class ContactUsMailApi(APIView):
    def sendmail(self, request):

        c = {
            'email': request.data['email'],
            'domain': request.META['HTTP_HOST'],
            'site_name': 'Bebras Admin',
            'protocol': 'http',
        }
        subject_template_name = 'Customer Queries';
        fromaddr = "softcornercummins@gmail.com"
        toaddr = "softcornercummins@gmail.com"
        mail = MIMEMultipart()
        mail['From'] = fromaddr
        mail['To'] = toaddr
        mail['Subject'] = subject_template_name
        body = " Customer name: "+request.data['name']+"\n Customer email: "+request.data['email']+ \
        "\n Query suject:"+request.data['subject']+"\n Query: \n"+request.data['message']
        mail.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(fromaddr, 'softcorner@2020')
        text = mail.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

    def post(self, request, *args, **kwargs):
        print((request.data))
        if request.data['email']:
            self.sendmail(request)
            return Response("Thank you! Our helpdesk will contact you within 24 hours.")
        else:
            return Response("Error",status=404)
class UserResultViewAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserViewSerializer
    def getTotalscore(competitionAgeid):
      totalscore=0
      compques=competitionQuestion.objects.filter(competitionAgeID=competitionAgeid)
      for ques in compques:
          competition_MarkS=competition_MarkScheme.objects.get(competitionAgeID=competitionAgeid,questionLevelCodeID=ques.questionLevelCodeID)
          totalscore=totalscore+competition_MarkS.correctMarks
      return totalscore
    def get(self, request, format=None):
      try:
        current_user = request.user
        response=[]
        cmps=studentEnrollment.objects.filter(userID=current_user.userID)
        if cmps.exists():
          for c in cmps:
            userdata={}
            userdata['loginID']=current_user.loginID
            userdata['userName']=current_user.userName
            userdata['competitionName']=c.competitionAgeID.competitionID.competitionName
            userdata['score']=c.score
            totalscore=UserResultViewAPI.getTotalscore(c.competitionAgeID)
            userdata['Totalscore']=totalscore
            response.append(userdata)
            print("TotalScore ",totalscore)
          return JsonResponse(response, safe=False)
        else:
          return Response("You have not registered for any competitions in any Competitions" ,status=404)
      except Exception as e:
        return HttpResponse(e,status=401)
class AllUserResultViewAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserViewSerializer
    def getTotalscore(competitionAgeid):
      totalscore=0
      compques=competitionQuestion.objects.filter(competitionAgeID=competitionAgeid)
      for ques in compques:
          competition_MarkS=competition_MarkScheme.objects.get(competitionAgeID=competitionAgeid,questionLevelCodeID=ques.questionLevelCodeID)

          totalscore=totalscore+competition_MarkS.correctMarks
      return totalscore
    def get(self, request, format=None):
      try:

        print("Currently logged in ",request.user.userID)
        userroles=UserRole.objects.filter(RoleID=StudentRoleID).values_list('userID', flat=True)
        test_ids=list(userroles)
        users = User.objects.filter(userID__in=test_ids,created_by=request.user.loginID)
        response=[]
        for current_user in users:
          print(current_user.userID)
          try:
            cmps=studentEnrollment.objects.filter(userID=current_user.userID)
            for c in cmps:
              userdata={}
              if c.score==999:
                print("enrolled but not attempted")
              else:
                userdata['loginID']=current_user.loginID
                userdata['username']=current_user.username
                userdata['competitionName']=c.competitionAgeID.competitionID.competitionName
                userdata['ageGroup']=c.competitionAgeID.AgeGroupClassID.AgeGroupID.AgeGroupName
                userdata['class']=c.schoolClassID.classNumber
                userdata['score']=c.score
                totalscore=AllUserResultViewAPI.getTotalscore(c.competitionAgeID)
                userdata['Totalscore']=totalscore
                response.append(userdata)
          except studentEnrollment.DoesNotExist:
            print("Not enrolled")

        return JsonResponse(response, safe=False)
      except Exception as e:
        return HttpResponse(e,status=401)
