from django.db import models
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,AbstractUser,UserManager as AbstractUserManager
from phonenumber_field.modelfields import PhoneNumberField
from com.models import *
import datetime


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,username,password,gender,birthdate,phone=None,email=None,loginID=None):
        try:
            if not username:
                raise ValueError("No username")
            if not loginID:
                raise ValueError("No loginID")
            if not password:
                raise ValueError("No Password")
            if not gender:
                raise ValueError("No gender")

            usr_obj = self.model(email=self.normalize_email(email),username=username,password=password,gender=gender,birthdate=birthdate,loginID=loginID,phone=phone)
            usr_obj.save(using=self._db)
            return usr_obj
        except Exception as e:
            print(e)
            return Exception("Can't save into database")

class User(AbstractBaseUser):
    userID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    loginID = models.CharField(max_length=255,null=False, unique=True)
    password = models.CharField(max_length=500)
    gender = models.ForeignKey(code,related_name='Gender',db_column='gender',to_field='codeID',on_delete=models.CASCADE)
    birthdate = models.DateField(null=True)
    phone = PhoneNumberField(null=True)
    email = models.CharField(max_length=70,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, default='default value')
    modified_on = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=50, default='default value')
    is_active = models.ForeignKey(code,related_name='is_active',db_column='is_active',default=106001,to_field='codeID',on_delete=models.CASCADE)
    USERNAME_FIELD = 'loginID'
    REQUIRED_FIELDS = ['username','password','gender']
    objects = UserManager()

class Role(models.Model):
    RoleID = models.IntegerField(primary_key=True)
    RoleName = models.CharField(max_length=20)
    RoleDescription = models.TextField()

class UserRole(models.Model):
    userRoleID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User,db_column='userID',to_field='userID',on_delete=models.CASCADE)
    RoleID = models.ForeignKey(Role,db_column='roleID',to_field='RoleID',on_delete=models.CASCADE)


class UserRoleLocation(models.Model):
    userRoleLocationID = models.AutoField(db_column='userRoleLocationID', primary_key=True)
    userRoleID = models.ForeignKey(UserRole, to_field='userRoleID', on_delete=models.CASCADE,db_column='userRoleID')
    locationTypeCodeID = models.ForeignKey(code, db_column='locationTypeCodeID',default=109001, to_field='codeID',on_delete=models.CASCADE)
    locationObjectID = models.IntegerField(null=False)
