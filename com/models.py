from django.db import models
from django.utils import timezone
import datetime
from phonenumber_field.modelfields import PhoneNumberField

class Countries(models.Model):
    countryID=models.AutoField(primary_key=True)
    iso = models.CharField(max_length=2,null=False)
    name = models.CharField(max_length=80)
    nicename = models.CharField(max_length=80)
    iso3 = models.CharField(max_length=3, blank=True, null=True)
    numcode = models.SmallIntegerField(blank=True, null=True)
    phonecode = models.IntegerField()

class States(models.Model):
  stateID=models.AutoField(primary_key=True)
  name = models.CharField(max_length=100,null=False)
  countryID = models.ForeignKey(Countries, db_column='countryID', to_field='countryID',on_delete=models.CASCADE)

class Districts(models.Model):
    districtID = models.AutoField(primary_key=True)
    stateID = models.ForeignKey(States, db_column='stateID',on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)

class Address(models.Model):
    addressID = models.AutoField(db_column='AddressID', primary_key=True)
    line1 = models.TextField(db_column='Line1', null=False)
    line2 = models.TextField(db_column='Line2', null=False)
    city = models.CharField(max_length=20, null=False)
    districtID = models.ForeignKey(Districts, db_column='districtID',on_delete=models.CASCADE)
    stateID = models.ForeignKey(States, db_column='stateID',on_delete=models.CASCADE)
    pincode = models.IntegerField()
    latitude = models.DecimalField(max_digits=25,null=True, decimal_places=20)
    longitude = models.DecimalField(max_digits=25,null=True, decimal_places=20)
    countryID = models.ForeignKey(Countries, db_column='countryID', to_field='countryID',on_delete=models.CASCADE)

class codeGroup(models.Model):
    codeGroupID=models.IntegerField(db_column='codeGroupID',primary_key=True)
    codeGroupName=models.CharField(db_column='codeGroupName',max_length=100, null=False)

class code(models.Model):
    codeID=models.IntegerField(db_column='codeID',primary_key=True)
    codeGroupID=models.ForeignKey(codeGroup, db_column='codeGroupID', to_field='codeGroupID',on_delete=models.CASCADE)
    codeName=models.CharField(db_column='codeName',max_length=100, null=False)

class school(models.Model):
    schoolID=models.AutoField(db_column='schoolID',primary_key=True)
    schoolName=models.CharField(db_column='schoolName',max_length=100, null=False)
    schoolTypeCodeID=models.ForeignKey(code,related_name='schoolType', db_column='schoolTypeCodeID', to_field='codeID',on_delete=models.CASCADE)
    addressID=models.ForeignKey(Address, db_column='addressID', to_field='addressID',on_delete=models.CASCADE)
    schoolGroupID = models.ForeignKey(code,related_name='schoolGroupCode',db_column='schoolGroupID', to_field='codeID',on_delete=models.CASCADE)
    UDISEcode=models.CharField(max_length=11,null=False)
    tag=models.CharField(max_length=100)
    phone=PhoneNumberField(null=False)
    registered_By=models.CharField(max_length=100,null=False)
    registered_On=models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=50, default='default value')

class schoolClass(models.Model):
    schoolClassID=models.AutoField(db_column='schoolClassID',primary_key=True)
    schoolID=models.ForeignKey(school, db_column='schoolID', to_field='schoolID',on_delete=models.CASCADE)
    classNumber=models.IntegerField(db_column='classNumber', null=False)

class Class(models.Model):
    classID=models.AutoField(db_column='classID',primary_key=True)
    classNo=models.IntegerField(db_column='classNo', null=False)
