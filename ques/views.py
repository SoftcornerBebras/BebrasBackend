from rest_framework.views import APIView
from .models import *
from .serializers import *
from com.models import *
from rest_framework.response import Response
from BebrasBackend.pagination import *
from knox.auth import TokenAuthentication
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView
from BebrasBackend.constants import *
from django.db.models import Q

class ViewImage(APIView):                            #View Images Per Question API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, **kwargs):
        try:
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
        except Exception as e:
            return Response(e,status=500)

class UserProfileQuesTimeline(APIView):                      #Get single user timeline for ques API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, **kwargs):
        try:
            usrdata=questionTranslation.objects.filter(modified_by=kwargs['loginID'])
            serializer = GetTranslatedQuestionDetail(usrdata,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e,status=500)

class QuestionPageView(APIView):                  # Get all Questions API
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            queryset = correctOption.objects.all().order_by('-questionTranslationID__modified_on')
            paginator = CustomPagination()
            response = paginator.generate_response(queryset,GetCorrectOption,request)
            qtransIds = []
            langs = []
            optTrans = []
            if len(response.data) != 0:
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
        except Exception as e:
            return Response(e,status=500)


class OptionView(APIView):                       #Get All optionsAPI
      authentication_classes = (TokenAuthentication, )
      permission_classes = (permissions.IsAuthenticated,)

      def get(self, request, **kwargs):
        try:
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
        except Exception as e:
            return Response(e,status=500)

class ViewQuestionSkills(APIView):                   # Get CS skills per Ques API
      authentication_classes = (TokenAuthentication, )
      permission_classes = (permissions.IsAuthenticated,)

      def get(self,request,**kwargs):
          try:
              lists = question.objects.filter(questionID=kwargs['questionID'])
              serializer = GetQuestionSkills(lists, many=True)
              skills = serializer.data[0]['cs_skills'].split(",")
              l1=[]
              for i in range(0,len(skills)):
                 l1.append(code.objects.get(codeID=skills[i]).codeName)
              return Response(l1)
          except Exception as e:
            return Response(e,status=500)

class ViewTraslations(APIView):                           #Get translations per Ques API
      authentication_classes = (TokenAuthentication, )
      permission_classes = (permissions.IsAuthenticated,)

      def get(self,request,**kwargs):
          try:
              lists = questionTranslation.objects.filter(questionID=kwargs['questionID']).values_list('questionTranslationID', flat=True)
              query= correctOption.objects.filter(questionTranslationID__in = lists)
              serializer = GetCorrectOption(query,many=True)
              optTransID = []
              if serializer.data[0]['ansText'] == None:
                  for ques in range(0,len(serializer.data)):
                      opts = option.objects.filter(questionID = serializer.data[ques]['questionTranslationID']['questionID']['questionID']).values_list('optionID', flat=True)
                      print(opts)
                      codeID = code.objects.get(codeName = serializer.data[ques]['questionTranslationID']['languageCodeID']['codeName'])
                      opttrans = optionTranslation.objects.filter(optionID__in = opts,languageCodeID = codeID).values_list('optionTranslationID', flat=True)
                      optTransID = optTransID + list(opttrans)
              optTrans = optionTranslation.objects.filter(optionTranslationID__in = optTransID)
              serializerF = GetAllTranslatedOptions(optTrans,many=True)
              return Response({
                "Questions":serializer.data,
                "Options":serializerF.data
            })
          except Exception as e:
            return Response(e,status=500)


class QuestionSearch(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        try:
            feed = request.data['feed']
            codes = code.objects.filter(Q(codeName__icontains = feed)).values_list('codeID', flat=True)
            codeID = list(codes)
            country = Countries.objects.filter(Q(nicename__icontains = feed)).values_list('countryID',flat=True)
            countryID = list(country)
            ques = question.objects.filter(Q(domainCodeID__in = codeID) |Q( questionTypeCodeID__in = codeID) | Q(countryID__in = countryID)).values_list('questionID', flat=True)
            quesID = list(ques)
            quesTrans = questionTranslation.objects.filter(Q(questionID__in = quesID) | Q(translation__icontains = feed) | Q(Identifier__icontains = feed) | Q(languageCodeID__in = codeID)).values_list('questionTranslationID', flat=True)
            quesTransID = list(quesTrans)
            query= correctOption.objects.filter(questionTranslationID__in = quesTransID)
            serializer = GetCorrectOption(query,many=True)
            finalQues = questionTranslation.objects.filter(Q(questionID__in = quesID) | Q(translation__icontains = feed) | Q(Identifier__icontains = feed) | Q(languageCodeID__in = codeID)).values_list('questionID', flat=True)
            finalQuesID = list(finalQues)
            opts = option.objects.filter(questionID__in=finalQuesID).values_list('optionID', flat=True)
            optList = list(opts)
            langCodes = questionTranslation.objects.filter(Q(questionID__in = quesID) | Q(translation__icontains = feed) | Q(Identifier__icontains = feed) | Q(languageCodeID__in = codeID)).values_list('languageCodeID', flat=True)
            lang = list(langCodes)
            optTrans = optionTranslation.objects.filter(optionID__in=optList,languageCodeID__in = lang)
            serializerF = GetAllTranslatedOptions(optTrans,many=True)
            return Response({
            "Questions":serializer.data,
            "Options":serializerF.data
        })
        except Exception as e:
            print(e)
            return Response(e,status=500)

class EditPreviousQuestion(APIView):

    def get(self,request):

        for ques in questionTranslation.objects.all():
            string = ques.translation['background']
            subs = "54.196.61.229"
            ques.translation['background'] = string.replace('3.84.169.90', subs)
            string1 = ques.translation['explanation']
            subs = "54.196.61.229"
            ques.translation['explanation'] = string1.replace('3.84.169.90', subs)
            ques.save()
        return Response(status=200)
