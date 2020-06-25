from rest_framework import serializers
from .models import *
from com.models import *
from com.serializers import *
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import exceptions
from datetime import *
from django.contrib.auth.models import User
from .password_encryption import encrypt,decrypt
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    is_active = CodeSerializer()
    gender = CodeSerializer()
    class Meta:
        model = User
        fields = ('userID','loginID','username','gender','email','birthdate','modified_on','modified_by','created_by','created_on','phone','is_active')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('RoleID', 'RoleName')

class UserRoleSerializer(serializers.ModelSerializer):

    userID = UserSerializer(read_only=True)
    RoleID = RoleSerializer(read_only=True)

    class Meta:
        model = UserRole
        fields = ('userRoleID', 'userID','RoleID')


class LogSerializer(serializers.Serializer):
    loginID = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        loginID = data.get("loginID", "")
        password = data.get("password", "")

        if loginID and password:
            user = User.objects.get(loginID = loginID)
            decrypt_pass = decrypt(user.password)
            if decrypt_pass==password:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated."
                    data["user"] = ""
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials."
                data["user"] = ""
                raise exceptions.ValidationError(msg)

        else:
            msg = "Must provide username and password both."
            data["user"] = ""
            raise exceptions.ValidationError(msg)
        return data

class UserInsertUpdateSerializer(serializers.ModelSerializer):
    is_active = CodeSerializer()
    gender = CodeSerializer()
    class Meta:
        model = User
        fields = ('loginID','username','password','birthdate','gender','email','phone','created_by','modified_by','modified_on','is_active')

    def update(self,instance,validated_data):
        instance.loginID = validated_data.get('loginID',instance.loginID)
        instance.birthdate = validated_data.get('birthdate',instance.birthdate)
        gender = validated_data.get('gender')
        genderID = code.objects.get(codeName=gender['codeName'])
        validated_data['gender']= genderID
        instance.gender = validated_data.get('gender',instance.gender)
        instance.phone = validated_data.get('phone',instance.phone)
        instance.modified_by =validated_data.get('username',instance.username)
        instance.modified_on = datetime.now().date()
        instance.save()
        return instance


class RoleInsertUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('RoleName',)

class UserRoleInsertUpdateSerializer(serializers.ModelSerializer):
    userID = UserInsertUpdateSerializer()
    RoleID = RoleInsertUpdateSerializer()


    class Meta:
        model = UserRole
        fields = '__all__'

    def create(self, validated_data):
        User_data = validated_data.pop('userID')
        role_data = validated_data.pop('RoleID')
        roleID = Role.objects.get(RoleName=role_data['RoleName'])
        password = encrypt(User_data['password'])
        User_data['password'] = password
        active = User_data['is_active']
        statusID = code.objects.get(codeName=active['codeName'])
        User_data['is_active'] = statusID
        gender = User_data['gender']
        genderID = code.objects.get(codeName=gender['codeName'])
        User_data['gender'] = genderID
        x = User(**User_data)
        x.created_on = datetime.now()
        x.modified_on = datetime.now().date()
        x.save()
        user = UserRole.objects.create(userID=x,RoleID = roleID, **validated_data)
        return user


    def update(self, instance, validated_data):
        User_data = validated_data.pop('userID')
        Role_data = validated_data.pop('RoleID')
        user = (instance.userID)
        role = (instance.RoleID)
        user.username = User_data.get('username',user.username)
        user.birthdate = User_data.get('birthdate',user.birthdate)
        user.email = User_data.get('email',user.email)
        user.phone = User_data.get('phone',user.phone)
        user.modified_on = datetime.now().date()
        user.modified_by = User_data.get('modified_by',user.modified_by)
        gender = code.objects.get(codeName=User_data['gender']['codeName'])
        User_data['gender'] = gender
        user.gender = User_data.get('gender',user.gender)
        active = code.objects.get(codeName=User_data['is_active']['codeName'])
        User_data['is_active'] = active
        user.is_active = User_data.get('is_active',user.is_active)
        if Role_data['RoleName'] != 'Student':
            user.loginID = User_data.get('email',user.email)
        else:
            user.loginID = User_data.get('loginID',user.loginID)
        user.save()
        rol = Role.objects.get(RoleName=Role_data['RoleName'])
        instance.RoleID = rol
        instance.save()
        return instance



class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('loginID','password')

    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)
        password = encrypt(instance.password)
        instance.password = password
        instance.save()
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserRoleLocationSerializer(serializers.ModelSerializer):
    userRoleID = UserRoleSerializer()
    locationTypeCodeID=CodeSerializer()
    class Meta:
        model = UserRoleLocation
        fields = ('userRoleLocationID', 'userRoleID','locationTypeCodeID','locationObjectID')



#user portal


class AddUserRoleSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserRole
    fields = ( 'userID','RoleID')

class StudentSerializer(serializers.ModelSerializer):
   class Meta:
        model = User
        #fields = '__all__'
        fields = ( 'username','loginID','password')

class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'username','loginID','birthdate')

class RegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ( 'username','password','gender','birthdate','phone','email','loginID')
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    print("IN SERIALIZER",validated_data)
    user = User.objects.create_user(validated_data['username'], validated_data['password'],validated_data['gender'],validated_data['birthdate'],validated_data['phone'],validated_data['email'],validated_data['loginID'])
    print("user",user)
    return user

class AddUserRoleLocationSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserRoleLocation
    fields = ( 'userRoleID','locationTypeCodeID','locationObjectID')

class LoginSerializer(serializers.Serializer):
  class Meta:
    model = User
    fields = ( 'loginID','password')
