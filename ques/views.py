from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from BebrasBackend.pagination import *
from knox.auth import TokenAuthentication
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView
from BebrasBackend.constants import *

class ViewImage(APIView):                            #View Images Per Question API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, **kwargs):
        coderef = code.objects.get(codeName='ImageAnsExplanation')
        qimg = Image.objects.filter(ObjectID=kwargs['ObjectID'],ImageTypeCodeID=coderef.codeID)
        serializer = GetImages(qimg, many=True)
        opt = option.objects.filter(questionID=kwargs['ObjectID'])
        coderef1 = code.objects.get(codeName='ImageOption')
        if(opt.exists()):
            serializero = GetOptions(opt, many=True)
            oimg1 = Image.objects.filter(ObjectID=serializero.data[0]['optionID'],ImageTypeCodeID=coderef1.codeID)
            serializer1 = GetImages(oimg1, many=True)
            oimg2 = Image.objects.filter(ObjectID=serializero.data[1]['optionID'],ImageTypeCodeID=coderef1.codeID)
            serializer2 = GetImages(oimg2, many=True)
            oimg3 = Image.objects.filter(ObjectID=serializero.data[2]['optionID'],ImageTypeCodeID=coderef1.codeID)
            serializer3 = GetImages(oimg3, many=True)
            oimg4 = Image.objects.filter(ObjectID=serializero.data[3]['optionID'],ImageTypeCodeID=coderef1.codeID)
            serializer4 = GetImages(oimg4, many=True)
            return Response({
            "qimg": serializer.data,
            "oimg1": serializer1.data,
            "oimg2": serializer2.data,
            "oimg3": serializer3.data,
            "oimg4": serializer4.data
            })
        else:
             return Response({
            "qimg": serializer.data,
            "oimg1": "empty",
            })

class UserProfileQuesTimeline(APIView):                      #Get single user timeline for ques API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, **kwargs):
        usrdata=questionTranslation.objects.filter(modified_by=kwargs['loginID'])
        serializer = GetTranslatedQuestionDetail(usrdata,many=True)
        return Response(serializer.data)

class QuestionPageView(APIView):                  # Get all Questions API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        queryset = correctOption.objects.all()
        paginator = CustomPagination()
        response = paginator.generate_response(queryset,GetCorrectOption,request)
        return Response(response.data)


class OptionView(APIView):                       #Get All optionsAPI
      authentication_classes = (TokenAuthentication, )
      permission_classes = (permissions.IsAuthenticated,)

      def get(self, request, **kwargs):
        quesList.clear()
        optList.clear()
        corrOpt = correctOption.objects.filter(correctOptionID__range=(kwargs['limit1'],kwargs['limit2'])).filter(ansText=None)
        serializer = GetCorrectOption(corrOpt,many=True)
        lang = []
        for i in range(0,serializer.data.__len__()):
              quesList.append(serializer.data[i]['questionTranslationID']['questionID']['questionID'])
              codeRef = code.objects.get(codeName =serializer.data[i]['questionTranslationID']['languageCodeID']['codeName'] )
              lang.append(codeRef.codeID)
        opts = option.objects.filter(questionID__in=quesList)
        serializerO = GetOptionsID(opts,many=True)
        for i in range(0,serializerO.data.__len__()):
              optList.append(serializerO.data[i]['optionID'])
        optTrans = optionTranslation.objects.filter(optionID__in=optList,languageCodeID__in = lang)
        serializerF = GetAllTranslatedOptions(optTrans,many=True)
        return Response(serializerF.data)

class ViewQuestionSkills(APIView):                   # Get CS skills per Ques API
      authentication_classes = (TokenAuthentication, )
      permission_classes = (permissions.IsAuthenticated,)

      def get(self,request,**kwargs):
          lists = question.objects.filter(questionID=kwargs['questionID'])
          serializer = GetQuestionSkills(lists, many=True)
          skills = serializer.data[0]['cs_skills'].split(",")
          l1=[]
          for i in range(0,len(skills)):
             l1.append(code.objects.get(codeID=skills[i]).codeName)
          return Response(l1)

class ViewTraslations(APIView):                           #Get translations per Ques API
      authentication_classes = (TokenAuthentication, )
      permission_classes = (permissions.IsAuthenticated,)

      def get(self,request,**kwargs):
          list = questionTranslation.objects.filter(questionID=kwargs['questionID'])
          serializer = GetTranslatedQuestionDetail(list,many=True)
          return Response(serializer.data)


class GetQuesYearWise(APIView):                                      #Get all Ques YearWise API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,**kwargs):
        quesTransList = questionTranslation.objects.filter(Identifier__icontains= kwargs['year'])
        quesList = []
        for i in range(0,len(quesTransList)):
            quesList.append(quesTransList[i].questionTranslationID)

        corroptlist = correctOption.objects.filter(questionTranslationID__in = quesList)
        paginator = CustomPagination()
        response = paginator.generate_response(corroptlist,GetCorrectOption,request)
        qtransIds = []
        langs = []
        for i in range(0,len(response.data['results'])):
            qtransIds.append(response.data['results'][i]['questionTranslationID']['questionID']['questionID'])
            codeRef = code.objects.get(codeName=response.data['results'][i]['questionTranslationID']['languageCodeID']['codeName'])
            langs.append(codeRef.codeID)
        opts = option.objects.filter(questionID__in=qtransIds)
        serializerO = GetOptionsID(opts,many=True)
        for i in range(0,serializerO.data.__len__()):
              optList.append(serializerO.data[i]['optionID'])
        optTrans = optionTranslation.objects.filter(optionID__in=optList,languageCodeID__in = langs)
        serializerF = GetAllTranslatedOptions(optTrans,many=True)
        return Response({
            "Questions":response.data,
            "Options":serializerF.data
        })
