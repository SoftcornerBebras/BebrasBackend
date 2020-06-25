from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from usr.serializers import *
from usr.models import *
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from cmp.models import *
from ques.models import *
from cmp.serializers import *
from com.models import *
from BebrasBackend.constants import *
from com.serializers import *


class CountryNameAPI(APIView):
    permission_classes = [
      permissions.AllowAny,
    ]
    def get(self, request, format=None):
      try:
        countries = Countries.objects.all().values_list('nicename', flat=True)
        return JsonResponse({"countries":list(countries)},safe=True)
      except Exception as e:
        return HttpResponse(e,status=404)
  # Get All School Names API
class SchoolNameAPI(APIView):

    permission_classes = [
      permissions.IsAuthenticated,
    ]
    def get(self, request, format=None):
      try:
        print(request.user.userID)
        usrrole=UserRole.objects.get(userID=request.user.userID)
        usrroleLocation=UserRoleLocation.objects.get(userRoleID=usrrole.userRoleID)

        school_names = school.objects.filter(schoolID=usrroleLocation.locationObjectID)
        if school_names:
          address=Address.objects.get(addressID=school_names.addressID)
          serializer=AddSchoolSerializer(school_names)

          return JsonResponse({"schoolName":serializer.data,"city":address.city},safe=True)
        else:
          return Response("No schools in Database")
      except Exception as e:
        return HttpResponse(e,status=404)

  # Get All State Names API
class StateNameAPI(APIView):
    permission_classes = [permissions.AllowAny,
    ]
    def post(self, request):
      try:
        print(request.data)
        country=Countries.objects.get(name=request.data['country'])
        states=States.objects.filter(countryID=country.countryID).values_list('name', flat=True)
        return JsonResponse({"states":list(states)}, safe=False)
      except Exception as e:
        return HttpResponse(e,status=404)
class SchoolClassesAPI(APIView):

    permission_classes = [
      permissions.IsAuthenticated,
    ]
    def get(self, request):
      try:
        print(request.data)
        userrole=UserRole.objects.get(userID=request.user.userID)
        userrolelocation=UserRoleLocation.objects.get(userRoleID=userrole.userRoleID)
        print(userrolelocation.locationObjectID)
        School=school.objects.get(schoolID=userrolelocation.locationObjectID)
        schoolclass=schoolClass.objects.filter(schoolID=School.schoolID).values_list('classNumber', flat=True)
        return JsonResponse({"schoolClasses":list(schoolclass)}, safe=False)
      except Exception as e:
        return HttpResponse(e,status=404)

  # Get All Cmp Names API
class CompetitionNameForCertificatesAPI(APIView):

    permission_classes = [
      permissions.IsAuthenticated,
    ]
    def post(self, request):
      try:
        print(request.data)
        cmpNames=[]
        compAge=competitionAge.objects.all()
        print(list(compAge))
        for data in compAge:
          endDate=data.competitionID.endDate
          if endDate.date() < datetime.now().date() and data.competitionID.competitionType.codeName==main_challenge:
            print(data.competitionID.competitionName)
            sclassid=data.AgeGroupClassID.ClassID.classID
            if sclassid==int(request.data['class_id']):
                cmpNames.append(data.competitionID.competitionName)
                print(cmpNames)
        cmpNames=list(set(cmpNames))
        if len(cmpNames)==0:
          return Response("No competitions to show, either they are upcoming or not  finished!",status=404)
        return JsonResponse({"cmp_names":cmpNames}, safe=False)
      except Exception as e:
        return HttpResponse(e,status=404)
class AgeGroupNameAPI(APIView):

    permission_classes = [
      permissions.IsAuthenticated,
    ]

    def post(self, request):
      try:
        print(request.data)
        AgeNames={}
        cmpageID=None
        print(request.data['competitionName'])
        compName=competition.objects.get(competitionName=request.data['competitionName'])
        print(compName)
        compAge=competitionAge.objects.filter(competitionID=compName.competitionID)
        print(list(compAge))
        for data in compAge:
          if data.AgeGroupClassID.ClassID.classNo==request.data['class_id']:
            print(data.AgeGroupClassID.AgeGroupID.AgeGroupName)
            AgeNames['age_names']=data.AgeGroupClassID.AgeGroupID.AgeGroupName
            cmpageID=data
            print(AgeNames)
            break
        if len(AgeNames)==0:
          return Response("No agegroups to show!",status=404)
        return JsonResponse(AgeNames, safe=False)
      except Exception as e:
        return HttpResponse(e,status=404)
class CompetitionNameAPI(APIView):

    permission_classes = [
      permissions.IsAuthenticated,
    ]
    def post(self, request):
      try:
        print(request.data)
        cmpNames=[]
        compAge=competitionAge.objects.all()
        print(list(compAge))
        for data in compAge:
          startDate=data.competitionID.startDate
          if startDate.date() > datetime.now().date() and data.competitionID.competitionType.codeName==main_challenge:
            print(data.competitionID.competitionName)
            sclassid=data.AgeGroupClassID.ClassID.classID
            if sclassid==int(request.data['class_id']):
                cmpNames.append(data.competitionID.competitionName)

        cmpNames=list(set(cmpNames))
        print(cmpNames)
        if len(cmpNames)==0:
          return Response("No competitions to show, either they are upcoming or already finished!",status=404)
        return JsonResponse({"cmp_names":cmpNames}, safe=False)
      except Exception as e:
        return HttpResponse(e,status=404)

  # Get All District Names API
class DistrictNameAPI(APIView):

    permission_classes = [
      permissions.AllowAny,
    ]
    def post(self, request):
      try:
        state=States.objects.get(name=request.data['state'])
        districts=Districts.objects.filter(stateID=state.stateID).values_list('name', flat=True)
        return JsonResponse({"districts":list(districts)}, safe=False)
      except Exception as e:
        return HttpResponse(e,status=404)
class SchoolGroupAPI(APIView):
    permission_classes = [
      permissions.AllowAny,
    ]
    def get(self, request, format=None):
      try:
        codes = code.objects.filter(codeGroupID=schoolGroupID)
        schoolGroupNames=[]
        for data in codes:
            schoolGroupNames.append(data.codeName)
        return JsonResponse({"schoolGroups":schoolGroupNames},safe=True)
      except Exception as e:
        return HttpResponse(e,status=404)
class SchoolTypeName(APIView):
    permission_classes = [
      permissions.AllowAny,
    ]
    def get(self, request, format=None):
      try:
        codes = code.objects.filter(codeGroupID=schooltype).values_list('codeName', flat=True)
        return JsonResponse({"schooltypenames":list(codes)},safe=True)
      except Exception as e:
        return HttpResponse(e,status=404)
class GenderName(APIView):
    permission_classes = [
      permissions.AllowAny,
    ]
    def get(self, request, format=None):
      try:
        codes = code.objects.filter(codeGroupID=gender).values_list('codeName', flat=True)
        return JsonResponse({"gender":list(codes)},safe=True)
      except Exception as e:
        return HttpResponse(e,status=404)
