from rest_framework import serializers
from .models import *
from datetime import *

class CountrySerializer(serializers.ModelSerializer):
  class Meta:
    model = Countries
    fields = ( 'nicename',)

class CountrysSerializer(serializers.ModelSerializer):
  class Meta:
    model = Countries
    fields = ( 'countryID','iso', 'name', 'nicename')

class StateSerializer(serializers.ModelSerializer):
  class Meta:
    model = States
    fields = ('stateID', 'name', 'countryID')

class DistrictSerializer(serializers.ModelSerializer):
  class Meta:
    model = Districts
    fields = ('districtID', 'name', 'stateID')

class AddressSerializer(serializers.ModelSerializer):
  districtID=DistrictSerializer()
  stateID=StateSerializer()
  countryID=CountrySerializer()
  class Meta:
    model = Address
    fields= ('addressID','line1','line2','city','districtID','stateID','pincode','latitude','longitude','countryID')

class CodeGroupSerializer(serializers.ModelSerializer):
  class Meta:
    model = codeGroup
    fields= ('codeGroupID','codeGroupName')

class CodeSerializer(serializers.ModelSerializer):

  class Meta:
    model =code
    fields =('codeName',)

class CodesSerializer(serializers.ModelSerializer):
  codeGroupID=CodeGroupSerializer()
  class Meta:
    model =code
    fields =('codeID','codeGroupID','codeName')

class SchoolViewSerializers(serializers.ModelSerializer):

  class Meta:
    model = school
    fields = ('schoolID','schoolName')

class SchoolSerializers(serializers.ModelSerializer):
  schoolTypeCodeID=CodeSerializer()
  addressID=AddressSerializer()
  schoolGroupID=CodeSerializer()
  class Meta:
    model = school
    fields = ('schoolID', 'schoolName','schoolTypeCodeID','schoolGroupID','addressID','UDISEcode','tag','phone','registered_By','registered_On','modified_by','modified_on')

  def update(self, instance, validated_data):
    print(validated_data)
    school_TypeCodeID = validated_data.pop('schoolTypeCodeID')
    school_group = validated_data.pop('schoolGroupID')
    addressID = validated_data.pop('addressID')
    countryID=addressID.pop('countryID')
    countryRef = Countries.objects.get(nicename=countryID['nicename'])
    stateID=addressID.pop('stateID')
    stateRefs = States.objects.filter(name=stateID['name'])
    stateRef=stateRefs[0];
    districtID=addressID.pop('districtID')
    districtRefs = Districts.objects.filter(name=districtID['name'],stateID=stateRef.stateID)
    districtRef=districtRefs[0]
    codenameID=school_TypeCodeID.pop('codeName')
    codegrp=codeGroup.objects.get(codeGroupName='school')
    codenameRef=code.objects.get(codeName=codenameID,codeGroupID=codegrp.codeGroupID)
    group=school_group.pop('codeName')
    groupRef = code.objects.get(codeName=group)
    modified_on = datetime.now()
    modified_by = validated_data.get('modified_by')
    instance.schoolName = validated_data.get('schoolName', instance.schoolName)
    instance.UDISEcode = validated_data.get('UDISEcode', instance.UDISEcode)
    instance.phone = validated_data.get('phone', instance.phone)
    instance.schoolTypeCodeID= validated_data.get('schoolTypeCodeID',codenameRef)
    instance.schoolGroupID= validated_data.get('schoolGroupID',groupRef)
    instance.modified_by = validated_data.get('modified_by',modified_by)
    instance.modified_on = modified_on
    instance.save()
    addID = (instance.addressID)
    addID.line1 = addressID.get('line1', addID.line1)
    addID.line2 = addressID.get('line2', addID.line2)
    addID.city = addressID.get('city', addID.city)
    addID.pincode = addressID.get('pincode', addID.pincode)
    addID.stateID = addressID.get('stateID',stateRef)
    addID.districtID = addressID.get('districtID',districtRef)
    addID.countryID = addressID.get('countryID',countryRef)
    addID.save()
    return instance


class SchoolClassSerializers(serializers.ModelSerializer):

  schoolID=SchoolSerializers()
  class Meta:
    model =schoolClass
    fields =('schoolClassID','schoolID','classNumber')

class ClassSerializer(serializers.ModelSerializer):

  class Meta:
    model = Class
    fields = ('classNo',)


#user portal


class AddAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ( 'line1','line2','city','districtID','stateID','pincode','latitude','longitude','countryID')

class AddSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = school
        fields = ( 'schoolName','schoolTypeCodeID','addressID','UDISEcode','phone','schoolGroupID')

class AddschoolClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = schoolClass
        fields = ( 'schoolID','classNumber')
