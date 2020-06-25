from django.shortcuts import render
from BebrasBackend.pagination import *
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from knox.auth import TokenAuthentication

class GetCountryView(APIView):                                    #Get All Countries API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        lists = Countries.objects.all()
        serializer = CountrysSerializer(lists,many=True)
        return Response(serializer.data)

class GetStateView(APIView):                                    #Get All States API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        lists = States.objects.all()
        serializer = StateSerializer(lists,many=True)
        return Response(serializer.data)

class GetDistrictView(APIView):               #Get All Districts API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        lists = Districts.objects.all()
        serializer = DistrictSerializer(lists,many=True)
        return Response(serializer.data)

class GetAddressView(APIView):              #Get Adrres of All Schools API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        lists = Address.objects.all()
        serializer = AddressSerializer(lists,many=True)
        return Response(serializer.data)


class GetCodeView(APIView):                  #Get ALL Codes API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        lists = code.objects.all()
        serializer = CodesSerializer(lists,many=True)
        return Response(serializer.data)

class GetCodeGroupView(APIView):              #Get ALL CodeGrp API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        lists = codeGroup.objects.all()
        serializer = CodeGroupSerializer(lists,many=True)
        return Response(serializer.data)

class GetSchoolView(APIView):                 #Get All Schools API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        lists = school.objects.all()
        serializer = SchoolSerializers(lists,many=True)
        return Response(serializer.data)

class GetSchoolClassView(APIView):                #Get All School Class API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,**kwargs):
        lists = schoolClass.objects.filter(schoolID=kwargs['SchoolID'])
        serializer = SchoolClassSerializers(lists,many=True)
        return Response(serializer.data)

class SchoolPageView(APIView):             #Get all Schools with Details API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        queryset = school.objects.all()
        paginator = CustomPagination()
        response = paginator.generate_response(queryset,SchoolSerializers,request)
        return Response(response.data)

class UpdateSchoolView(APIView):          #Update School Details API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, **kwargs):
        id = school.objects.get(schoolID=kwargs['schoolID'])
        serializers = SchoolSerializers(instance=id, data=request.data, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)


class GetQuestionTypeView(APIView):           #Get All QuesType API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        question = codeGroup.objects.get(codeGroupName='question')
        questiontypes = code.objects.filter(codeGroupID=question.codeGroupID)
        serializer = CodeSerializer(questiontypes,many=True)
        return Response(serializer.data)

class GetLanguageView(APIView):                #Get All Language API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        question = codeGroup.objects.get(codeGroupName='language')
        questiontypes = code.objects.filter(codeGroupID=question.codeGroupID)
        serializer = CodeSerializer(questiontypes,many=True)
        return Response(serializer.data)


class GetQuestionLevelView(APIView):             #Get All Queslevel API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        questionL = codeGroup.objects.get(codeGroupName='questionLevel')
        questionLevel = code.objects.filter(codeGroupID=questionL.codeGroupID)
        serializer = CodeSerializer(questionLevel,many=True)
        return Response(serializer.data)

class GetDomainView(APIView):                   #Get All Domain API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        Domain = codeGroup.objects.get(codeGroupName='domain')
        domainLevel = code.objects.filter(codeGroupID=Domain.codeGroupID)
        serializer = CodeSerializer(domainLevel,many=True)
        return Response(serializer.data)

class GetSkillsView(APIView):                      #Get All CS skills API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        skills = codeGroup.objects.get(codeGroupName='skills')
        csskills = code.objects.filter(codeGroupID=skills.codeGroupID)
        serializer = CodeSerializer(csskills,many=True)
        return Response(serializer.data)


class GetSchoolWiseClasses(APIView):                 #Get School wise Classes API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,**kwargs):
        classes = schoolClass.objects.filter(schoolID=kwargs['schoolID'])
        serializer= SchoolClassSerializers(classes,many=True)
        return Response(serializer.data)

class GetSchoolList(APIView):                        #Get school List API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        schools = school.objects.all()
        serializer= SchoolViewSerializers(schools,many=True)
        return Response(serializer.data)

class GetClassView(APIView):                      #Get All Classes API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        classes = Class.objects.all()
        serializer= ClassSerializer(classes,many=True)
        return Response(serializer.data)

class GetCmpTypes(APIView):                           #Get All Cmp Types API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        cmpType = codeGroup.objects.get(codeGroupName='competitionType')
        cmpTypes = code.objects.filter(codeGroupID=cmpType.codeGroupID)
        serializer = CodeSerializer(cmpTypes,many=True)
        return Response(serializer.data)

class InsertNewLanguage(APIView):                  #Insert New Language API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,requests):
        codegrpRef = codeGroup.objects.get(codeGroupName = 'language')
        codeRef = code.objects.filter(codeGroupID=codegrpRef.codeGroupID)
        s=0
        for i in range(0,len(codeRef)):
            if(str(codeRef[i].codeName).lower()==str(requests.data['language']).lower()):
                s=-1
                break
        if(s!=-1):
            code.objects.create(codeID = (codeRef[len(codeRef)-1].codeID+1),codeGroupID =codegrpRef,codeName=requests.data['language'] )
            s=200
        return Response(s)

class InsertNewDomain(APIView):                      #Insert New domain API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,requests):
        codegrpRef = codeGroup.objects.get(codeGroupName = 'domain')
        codeRef = code.objects.filter(codeGroupID=codegrpRef.codeGroupID)
        s = 0
        for i in range(0, len(codeRef)):
            if (str(codeRef[i].codeName).lower() == str(requests.data['domain']).lower()):
                s = -1
                break
        if(s!=-1):
            code.objects.create(codeID = (codeRef[len(codeRef)-1].codeID+1),codeGroupID =codegrpRef,codeName=requests.data['domain'] )
            s=200
        return Response(s)

class InsertNewLevel(APIView):                        #Insert New QuesLevel API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,requests):
        codegrpRef = codeGroup.objects.get(codeGroupName = 'questionLevel')
        codeRef = code.objects.filter(codeGroupID=codegrpRef.codeGroupID)
        s = 0
        for i in range(0, len(codeRef)):
            if (str(codeRef[i].codeName).lower() == str(requests.data['level']).lower()):
                s = -1
                break
        if(s!=-1):
            code.objects.create(codeID = (codeRef[len(codeRef)-1].codeID+1),codeGroupID =codegrpRef,codeName=requests.data['level'] )
            s=200
        return Response(s)

class InsertNewSkill(APIView):                         #Insert New Cs skill API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,requests):
        codegrpRef = codeGroup.objects.get(codeGroupName = 'skills')
        codeRef = code.objects.filter(codeGroupID=codegrpRef.codeGroupID)
        s = 0
        for i in range(0, len(codeRef)):
            if (str(codeRef[i].codeName).lower() == str(requests.data['skill']).lower()):
                s = -1
                break
        if (s != -1):
            code.objects.create(codeID = (codeRef[len(codeRef)-1].codeID+1),codeGroupID =codegrpRef,codeName=requests.data['skill'] )
            s=200
        return Response(s)

class InsertNewSchoolGroup(APIView):                          #Insert New School Group
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,requests):
        codegrpRef = codeGroup.objects.get(codeGroupName = 'schoolGroup')
        codeRef = code.objects.filter(codeGroupID=codegrpRef.codeGroupID)
        s = 0
        for i in range(0, len(codeRef)):
            if (str(codeRef[i].codeName).lower() == str(requests.data['schoolGroup']).lower()):
                s = -1
                break
        if (s != -1):
            code.objects.create(codeID = (codeRef[len(codeRef)-1].codeID+1),codeGroupID =codegrpRef,codeName=requests.data['schoolGroup'] )
            s=200
        return Response(s)

class GetStateCountryWise(APIView):             #Get State Country Wise API
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,**kwargs):
        country=Countries.objects.get(countryID=kwargs['countryID'])
        states=States.objects.filter(countryID=country.countryID)
        serializer= StateSerializer(states,many=True)
        return Response(serializer.data)


class GetDistrictStateWise(APIView):                #Get Districts State Wise API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,**kwargs):
        state=States.objects.get(stateID=kwargs['stateID'])
        districts=Districts.objects.filter(stateID=state.stateID)
        serializer= DistrictSerializer(districts,many=True)
        return Response(serializer.data)


class GetGroup(APIView):                              #Get School Groups API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
       group= codeGroup.objects.filter(codeGroupName="schoolGroup")
       print(group)
       groups=code.objects.filter(codeGroupID=group[0].codeGroupID)
       serializers=CodesSerializer(groups,many=True)
       return Response(serializers.data)

class SchoolPTimeline(APIView):                         #Get Single user Timeline for Schools
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, **kwargs):
        usrdata=school.objects.filter(modified_by=kwargs['loginID'])
        serializer = SchoolSerializers(usrdata,many=True)
        return Response(serializer.data)

class GetSchoolType(APIView):                             #Get All School Types API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
       type= codeGroup.objects.get(codeGroupName="school")
       types=code.objects.filter(codeGroupID=type.codeGroupID)
       serializers=CodesSerializer(types,many=True)
       return Response(serializers.data)
