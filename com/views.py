from django.shortcuts import render
from BebrasBackend.pagination import *
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from django.db.models import Q

class GetCountryView(APIView):                                    #Get All Countries API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            lists = Countries.objects.all().order_by('name')
            serializer = CountrysSerializer(lists,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)

class GetStateView(APIView):                                    #Get All States API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            lists = States.objects.all().order_by('name')
            serializer = StateSerializer(lists,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)

class GetDistrictView(APIView):               #Get All Districts API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            lists = Districts.objects.all().order_by('name')
            serializer = DistrictSerializer(lists,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)

class GetAddressView(APIView):              #Get Adrres of All Schools API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            lists = Address.objects.all()
            serializer = AddressSerializer(lists,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)


class GetCodeView(APIView):                  #Get ALL Codes API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            lists = code.objects.all()
            serializer = CodesSerializer(lists,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)

class GetCodeGroupView(APIView):              #Get ALL CodeGrp API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            lists = codeGroup.objects.all()
            serializer = CodeGroupSerializer(lists,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)

class GetSchoolView(APIView):                 #Get All Schools API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            lists = school.objects.all().order_by('schoolName')
            serializer = SchoolSerializers(lists,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)

class GetSchoolClassView(APIView):                #Get All School Class API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,**kwargs):
        try:
            lists = schoolClass.objects.filter(schoolID=kwargs['SchoolID'])
            serializer = SchoolClassSerializers(lists,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)

class SchoolPageView(APIView):             #Get all Schools with Details API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            queryset = school.objects.all().order_by('-schoolID')
            paginator = CustomPagination()
            response = paginator.generate_response(queryset,SchoolSerializers,request)
            return Response(response.data)
        except Exception as e:
            return Response(e,status=500)

class UpdateSchoolView(APIView):          #Update School Details API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, **kwargs):
        try:
            id = school.objects.get(schoolID=kwargs['schoolID'])
            serializers = SchoolSerializers(instance=id, data=request.data, partial=True)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data)
        except Exception as e:
            return Response(e,status=500)

class GetQuestionTypeView(APIView):           #Get All QuesType API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            question = codeGroup.objects.get(codeGroupName='question')
            questiontypes = code.objects.filter(codeGroupID=question.codeGroupID).order_by('codeName')
            serializer = CodeSerializer(questiontypes,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)

class GetLanguageView(APIView):                #Get All Language API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            question = codeGroup.objects.get(codeGroupName='language')
            questiontypes = code.objects.filter(codeGroupID=question.codeGroupID).order_by('codeName')
            serializer = CodeSerializer(questiontypes,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)


class GetQuestionLevelView(APIView):             #Get All Queslevel API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            questionL = codeGroup.objects.get(codeGroupName='questionLevel')
            questionLevel = code.objects.filter(codeGroupID=questionL.codeGroupID).order_by('codeName')
            serializer = CodeSerializer(questionLevel,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)

class GetDomainView(APIView):                   #Get All Domain API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            Domain = codeGroup.objects.get(codeGroupName='domain')
            domainLevel = code.objects.filter(codeGroupID=Domain.codeGroupID).order_by('codeName')
            serializer = CodeSerializer(domainLevel,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)

class GetSkillsView(APIView):                      #Get All CS skills API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            skills = codeGroup.objects.get(codeGroupName='skills')
            csskills = code.objects.filter(codeGroupID=skills.codeGroupID).order_by('codeName')
            serializer = CodeSerializer(csskills,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)


class GetSchoolWiseClasses(APIView):                 #Get School wise Classes API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,**kwargs):
        try:
            classes = schoolClass.objects.filter(schoolID=kwargs['schoolID'])
            serializer= SchoolClassSerializers(classes,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)

class GetSchoolList(APIView):                        #Get school List API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            schools = school.objects.all().order_by('schoolName')
            serializer= SchoolViewSerializers(schools,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)

class GetClassView(APIView):                      #Get All Classes API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            classes = Class.objects.all()
            serializer= ClassSerializer(classes,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)

class GetCmpTypes(APIView):                           #Get All Cmp Types API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            cmpType = codeGroup.objects.get(codeGroupName='competitionType')
            cmpTypes = code.objects.filter(codeGroupID=cmpType.codeGroupID).order_by('codeName')
            serializer = CodeSerializer(cmpTypes,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)

class InsertNewLanguage(APIView):                  #Insert New Language API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,requests):
        try:
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
        except Exception as e:
            return Response(e,status=500)

class InsertNewDomain(APIView):                      #Insert New domain API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,requests):
        try:
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
        except Exception as e:
            return Response(e,status=500)

class InsertNewLevel(APIView):                        #Insert New QuesLevel API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,requests):
        try:
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
        except Exception as e:
            return Response(e,status=500)

class InsertNewSkill(APIView):                         #Insert New Cs skill API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,requests):
        try:
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
        except Exception as e:
            return Response(e,status=500)

class InsertNewSchoolGroup(APIView):                          #Insert New School Group
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,requests):
        try:
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
        except Exception as e:
            return Response(e,status=500)

class GetStateCountryWise(APIView):             #Get State Country Wise API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,**kwargs):
        try:
            country=Countries.objects.get(countryID=kwargs['countryID'])
            states=States.objects.filter(countryID=country.countryID).order_by('name')
            serializer= StateSerializer(states,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)


class GetDistrictStateWise(APIView):                #Get Districts State Wise API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,**kwargs):
        try:
            state=States.objects.get(stateID=kwargs['stateID'])
            districts=Districts.objects.filter(stateID=state.stateID).order_by('name')
            serializer= DistrictSerializer(districts,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)


class GetGroup(APIView):                              #Get School Groups API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
       try:
           group= codeGroup.objects.filter(codeGroupName="schoolGroup")
           groups=code.objects.filter(codeGroupID=group[0].codeGroupID).order_by('codeName').exclude(codeName='Other')
           SchoolGrps = []
           if len(groups) != 0:
               for i in range(0,len(groups)):
                   grpdata = {"codeName":groups[i].codeName,
                           "codeID":groups[i].codeID}
                   SchoolGrps.append(grpdata)
           g = code.objects.get(codeName='Other',codeGroupID=group[0].codeGroupID)
           grpdata = {"codeName": g.codeName,
                      "codeID" : g.codeID}
           SchoolGrps.append(grpdata)
           return Response({"data":SchoolGrps})
       except Exception as e:
            return Response(e,status=500)

class SchoolPTimeline(APIView):                         #Get Single user Timeline for Schools
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, **kwargs):
        try:
            usrdata=school.objects.filter(modified_by=kwargs['loginID'])
            serializer = SchoolSerializers(usrdata,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)

class GetSchoolType(APIView):                             #Get All School Types API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
       try:
           type= codeGroup.objects.get(codeGroupName="school")
           types=code.objects.filter(codeGroupID=type.codeGroupID).order_by('codeName').exclude(codeName='Other')
           SchoolTyps = []
           if len(types) != 0:
               for i in range(0,len(types)):
                   typdata = {"codeName":types[i].codeName,
                           "codeID":types[i].codeID}
                   SchoolTyps.append(typdata)
           g = code.objects.get(codeName='Other',codeGroupID=type.codeGroupID)
           typdata = {"codeName": g.codeName,
                      "codeID" : g.codeID}
           SchoolTyps.append(typdata)
           return Response({"data":SchoolTyps})
       except Exception as e:
            return Response(e,status=500)

class SchoolSearch(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        try:
            feed = request.data['feed']
            state = States.objects.filter(Q(name__contains = feed)).values_list('stateID', flat=True)
            stateID = list(state)
            add = Address.objects.filter(Q(city__contains = feed) |Q( stateID__in = stateID)).values_list('addressID', flat=True)
            addressID = list(add)
            query= school.objects.filter(Q(schoolName__contains = feed) | Q(UDISEcode__contains = feed) | Q(addressID__in = addressID))
            serializer = SchoolSerializers(query,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)
