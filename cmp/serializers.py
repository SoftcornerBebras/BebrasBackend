from rest_framework import serializers
from .models import *
from rest_framework import exceptions
from com.serializers import *
from com.models import *
from ques.serializers import *
from ques.models import *
from usr.models import *
from usr.serializers import *
from .models import *
from datetime import *
import json
import collections
from BebrasBackend.constants import *

class InsertMcqQuesSerializer(serializers.ModelSerializer):
    questionTranslationID = GetTranslatedQuestion()
    optionTranslationID = GetTranslatedOptions()

    class Meta:
        model = correctOption
        fields = ('correctOptionID', 'questionTranslationID', 'optionTranslationID')

    def create(self, validated_data):
        quesTransID = validated_data.pop('questionTranslationID', None)
        quesID = quesTransID.pop('questionID', None)
        langCodeId = quesTransID.pop('languageCodeID', None)
        langCodeRef = code.objects.get(codeName=langCodeId['codeName'])
        identifier = quesTransID.get('Identifier',None)
        modified_by = quesTransID.pop('modified_by', None)
        countryId = quesID.pop('countryID', None)
        countryRef = Countries.objects.get(nicename=countryId['nicename'])
        domainCodeId = quesID.pop('domainCodeID', None)
        domainCodeRef = code.objects.get(codeName=domainCodeId['codeName'])
        quesTypeId = quesID.pop('questionTypeCodeID', None)
        quesTypeRef = code.objects.get(codeName=quesTypeId['codeName'])
        quesTranslation = quesTransID.pop('translation',None)
        skills = quesTranslation['quescsskills'].split(',')
        cs_skills=""
        cs_skills = str(code.objects.get(codeName=skills[0]).codeID)
        for i in range(1,len(skills)):
            cs_skills = cs_skills +","+str(code.objects.get(codeName=skills[i]).codeID)
        ques = question.objects.create(countryID=countryRef, domainCodeID=domainCodeRef, questionTypeCodeID=quesTypeRef,cs_skills=cs_skills)
        QuesAgeID = quesTranslation['quesAgeID']
        translation = quesTranslation['translation']
        imageID = quesTranslation['imageID']
        imageAnsID = quesTranslation['imageAnsID']
        AgeQID = QuesAgeID.pop('QuestionAgeID', None)
        if AgeQID['AgeGroupName']!="":
            ageGroupList = AgeQID['AgeGroupName'].split(',')
            ageGroupIDList = AgeQID['AgeGroupID'].split(',')
            questionLevelCodeID = QuesAgeID.pop('questionLevelCodeID', None)
            quesLevelList = questionLevelCodeID['codeName'].split(',')
        else:
             ageGroupList=[]
        if imageID['ImageName']!="":
            imageNameList = imageID['ImageName'].split(',')
            imageUrlList = imageID['uploadedFile'].split(',')
            imageTypeList = imageID['ImageTypeCodeID']['codeName'].split(',')
        else:
             imageNameList=[]
        if imageAnsID['ImageName']!="":
            imageANameList = imageAnsID['ImageName'].split(',')
            imageAUrlList = imageAnsID['uploadedFile'].split(',')
            imageATypeList = imageAnsID['ImageTypeCodeID']['codeName'].split(',')
        else:
            imageANameList=[]

        if len(imageANameList)>0:
            for i in range(0, len(imageANameList)):
                ImageTypeRef = code.objects.get(codeName=imageATypeList[i])
                img = Image.objects.create(ImageName=imageANameList[i], ImageTypeCodeID=ImageTypeRef, ObjectID=ques.questionID,
                                       uploadedFile=imageAUrlList[i])
        if len(ageGroupList)>0:
            for i in range(0, len(ageGroupList)):
                AgeGroupNameRef = AgeGroup.objects.get(AgeGroupName=ageGroupList[i],AgeGroupID=ageGroupIDList[i])
                quesLevelRef = code.objects.get(codeName=quesLevelList[i])
                AgeQues = QuestionAge.objects.create(AgeGroupID=AgeGroupNameRef, questionID=ques,
                                                             questionLevelCodeID=quesLevelRef)
        if len(imageNameList)>0:
            for i in range(0, len(imageNameList)):
                ImageTypeRef = code.objects.get(codeName=imageTypeList[i])
                if (ImageTypeRef.codeName == "ImageQuestion"):
                    img = Image.objects.create(ImageName=imageNameList[i], ImageTypeCodeID=ImageTypeRef, ObjectID=ques.questionID,
                                               uploadedFile=imageUrlList[i])
        modified_on = datetime.now().date()
        quesTrans = questionTranslation.objects.create(questionID=ques, languageCodeID=langCodeRef,
                                                       translation=translation,Identifier=identifier,modified_by=modified_by,
                                                       modified_on=modified_on)
        OptTransID = validated_data.pop('optionTranslationID', None)
        optID = OptTransID.pop('translationO')
        y = optID['translationO']
        if len(y['ansText'])==0:
            correctOpt = None
            if y['option1']['caption']['option'] == y['correctOption']:
                opt = option.objects.create(questionID=ques)
                y1 = y['option1']
                optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                            translationO=y1['caption'])

                correctOpt = optionTranslation.objects.get(optionTranslationID=optTrans.optionTranslationID, optionID=opt)
            else:
                opt = option.objects.create(questionID=ques)
                y1 = y['option1']
                optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                            translationO=y1['caption'])

            if y['option2']['caption']['option'] == y['correctOption']:
                opt = option.objects.create(questionID=ques)
                y1 = y['option2']
                optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                            translationO=y1['caption'])
                correctOpt = optionTranslation.objects.get(optionTranslationID=optTrans.optionTranslationID, optionID=opt)
            else:
                opt = option.objects.create(questionID=ques)
                y1 = y['option2']
                optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                            translationO=y1['caption'])

            if y['option3']['caption']['option'] == y['correctOption']:
                opt = option.objects.create(questionID=ques)
                y1 = y['option3']
                optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                            translationO=y1['caption'])
                correctOpt = optionTranslation.objects.get(optionTranslationID=optTrans.optionTranslationID, optionID=opt)
            else:
                opt = option.objects.create(questionID=ques)
                y1 = y['option3']
                optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                            translationO=y1['caption'])

            if y['option4']['caption']['option'] == y['correctOption']:
                opt = option.objects.create(questionID=ques)
                y1 = y['option4']
                optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                            translationO=y1['caption'])
                correctOpt = optionTranslation.objects.get(optionTranslationID=optTrans.optionTranslationID, optionID=opt)
            else:
                opt = option.objects.create(questionID=ques)
                y1 = y['option4']
                optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                            translationO=y1['caption'])

            corrOpt = correctOption.objects.create(questionTranslationID=quesTrans, optionTranslationID=correctOpt,
                                                   **validated_data)
        else:
            corrOpt = correctOption.objects.create(questionTranslationID=quesTrans, ansText=y['ansText'],
                                                   **validated_data)
        return corrOpt


class InsertMcqWithImagesQuesSerializer(serializers.ModelSerializer):
    questionTranslationID = GetTranslatedQuestion()
    optionTranslationID = GetTranslatedOptions()

    class Meta:
        model = correctOption
        fields = ('correctOptionID', 'questionTranslationID', 'optionTranslationID')

    def create(self, validated_data):
        quesTransID = validated_data.pop('questionTranslationID', None)
        quesID = quesTransID.pop('questionID', None)
        langCodeId = quesTransID.pop('languageCodeID', None)
        langCodeRef = code.objects.get(codeName=langCodeId['codeName'])
        modified_by = quesTransID.pop('modified_by', None)
        identifier = quesTransID.pop('Identifier', None)
        countryId = quesID.pop('countryID', None)
        countryRef = Countries.objects.get(nicename=countryId['nicename'])
        domainCodeId = quesID.pop('domainCodeID', None)
        domainCodeRef = code.objects.get(codeName=domainCodeId['codeName'])
        quesTypeId = quesID.pop('questionTypeCodeID', None)
        quesTypeRef = code.objects.get(codeName=quesTypeId['codeName'])
        quesTranslation = quesTransID.pop('translation',None)
        skills = quesTranslation['quescsskills'].split(',')
        cs_skills = ""
        cs_skills = str(code.objects.get(codeName=skills[0]).codeID)
        for i in range(1,len(skills)):
            cs_skills = cs_skills +","+str(code.objects.get(codeName=skills[i]).codeID)
        ques = question.objects.create(countryID=countryRef, domainCodeID=domainCodeRef, questionTypeCodeID=quesTypeRef,cs_skills=cs_skills)
        QuesAgeID = quesTranslation['quesAgeID']
        translation = quesTranslation['translation']
        imageID = quesTranslation['imageID']
        imageAnsID = quesTranslation['imageAnsID']
        AgeQID = QuesAgeID.pop('QuestionAgeID', None)
        if AgeQID['AgeGroupName']!="":
            ageGroupList = AgeQID['AgeGroupName'].split(',')
            ageGroupIDList = AgeQID['AgeGroupID'].split(',')
            questionLevelCodeID = QuesAgeID.pop('questionLevelCodeID', None)
            quesLevelList = questionLevelCodeID['codeName'].split(',')
        else:
             ageGroupList=[]
        if imageID['ImageName']!="":
            imageNameList = imageID['ImageName'].split(',')
            imageUrlList = imageID['uploadedFile'].split(',')
            imageTypeList = imageID['ImageTypeCodeID']['codeName'].split(',')
        else:
            imageNameList=[]
        if imageAnsID['ImageName']!="":
            imageANameList = imageAnsID['ImageName'].split(',')
            imageAUrlList = imageAnsID['uploadedFile'].split(',')
            imageATypeList = imageAnsID['ImageTypeCodeID']['codeName'].split(',')
        else:
            imageANameList=[]
        if len(imageANameList)>0:
            for i in range(0, len(imageANameList)):
                ImageTypeRef = code.objects.get(codeName=imageATypeList[i])
                img = Image.objects.create(ImageName=imageANameList[i], ImageTypeCodeID=ImageTypeRef, ObjectID=ques.questionID,
                                           uploadedFile=imageAUrlList[i])
        if len(ageGroupList)>0:
            for i in range(0, len(ageGroupList)):
                AgeGroupNameRef = AgeGroup.objects.get(AgeGroupName=ageGroupList[i],AgeGroupID=ageGroupIDList[i])
                quesLevelRef = code.objects.get(codeName=quesLevelList[i])
                AgeQues = QuestionAge.objects.create(AgeGroupID=AgeGroupNameRef, questionID=ques,
                                                             questionLevelCodeID=quesLevelRef)
        if len(imageNameList)>0:
            for i in range(0, len(imageNameList)):
                ImageTypeRef = code.objects.get(codeName=imageTypeList[i])
                if (ImageTypeRef.codeName == "ImageQuestion"):
                    img = Image.objects.create(ImageName=imageNameList[i], ImageTypeCodeID=ImageTypeRef, ObjectID=ques.questionID,
                                               uploadedFile=imageUrlList[i])
        modified_on = datetime.now().date()
        quesTrans = questionTranslation.objects.create(questionID=ques, languageCodeID=langCodeRef,
                                                       translation=translation, modified_by=modified_by,
                                                       modified_on=modified_on,Identifier=identifier)
        OptTransID = validated_data.pop('optionTranslationID', None)
        optID = OptTransID.pop('translationO')
        y = optID['translationO']
        correctOpt = None
        if y['option1']['caption']['option'] == y['correctOption']:
            opt = option.objects.create(questionID=ques)
            y1 = y['option1']
            optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                        translationO=y1['caption'])

            correctOpt = optionTranslation.objects.get(optionTranslationID=optTrans.optionTranslationID, optionID=opt)
            imagenameo = y1['imageID']['ImageName']
            imageurlo = y1['imageID']['uploadedFile']
            imagetype = y1['imageID']['ImageTypeCodeID']
            ImageTypeRef = code.objects.get(codeName=imagetype['codeName'])
            if (ImageTypeRef.codeName == "ImageOption"):
                img = Image.objects.create(ImageName=imagenameo, ImageTypeCodeID=ImageTypeRef, ObjectID=opt.optionID,
                                           uploadedFile=imageurlo)

        else:
            opt = option.objects.create(questionID=ques)
            y1 = y['option1']
            optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                        translationO=y1['caption'])
            imagenameo = y1['imageID']['ImageName']
            imageurlo = y1['imageID']['uploadedFile']
            imagetype = y1['imageID']['ImageTypeCodeID']
            ImageTypeRef = code.objects.get(codeName=imagetype['codeName'])
            if (ImageTypeRef.codeName == "ImageOption"):
                img = Image.objects.create(ImageName=imagenameo, ImageTypeCodeID=ImageTypeRef, ObjectID=opt.optionID,
                                           uploadedFile=imageurlo)
        if y['option2']['caption']['option'] == y['correctOption']:
            opt = option.objects.create(questionID=ques)
            y1 = y['option2']
            optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                        translationO=y1['caption'])
            correctOpt = optionTranslation.objects.get(optionTranslationID=optTrans.optionTranslationID, optionID=opt)
            imagenameo = y1['imageID']['ImageName']
            imageurlo = y1['imageID']['uploadedFile']
            imagetype = y1['imageID']['ImageTypeCodeID']
            ImageTypeRef = code.objects.get(codeName=imagetype['codeName'])
            if (ImageTypeRef.codeName == "ImageOption"):
                img = Image.objects.create(ImageName=imagenameo, ImageTypeCodeID=ImageTypeRef, ObjectID=opt.optionID,
                                           uploadedFile=imageurlo)

        else:
            opt = option.objects.create(questionID=ques)
            y1 = y['option2']
            optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                        translationO=y1['caption'])
            imagenameo =y1['imageID']['ImageName']
            imageurlo = y1['imageID']['uploadedFile']
            imagetype = y1['imageID']['ImageTypeCodeID']
            ImageTypeRef = code.objects.get(codeName=imagetype['codeName'])
            if (ImageTypeRef.codeName == "ImageOption"):
                img = Image.objects.create(ImageName=imagenameo, ImageTypeCodeID=ImageTypeRef, ObjectID=opt.optionID,
                                           uploadedFile=imageurlo)
        if y['option3']['caption']['option'] == y['correctOption']:
            opt = option.objects.create(questionID=ques)
            y1 = y['option3']
            optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                        translationO=y1['caption'])
            correctOpt = optionTranslation.objects.get(optionTranslationID=optTrans.optionTranslationID, optionID=opt)
            imagenameo = y1['imageID']['ImageName']
            imageurlo = y1['imageID']['uploadedFile']
            imagetype = y1['imageID']['ImageTypeCodeID']
            ImageTypeRef = code.objects.get(codeName=imagetype['codeName'])
            if (ImageTypeRef.codeName == "ImageOption"):
                img = Image.objects.create(ImageName=imagenameo, ImageTypeCodeID=ImageTypeRef, ObjectID=opt.optionID,
                                           uploadedFile=imageurlo)

        else:
            opt = option.objects.create(questionID=ques)
            y1 = y['option3']
            optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                        translationO=y1['caption'])
            imagenameo = y1['imageID']['ImageName']
            imageurlo = y1['imageID']['uploadedFile']
            imagetype = y1['imageID']['ImageTypeCodeID']
            ImageTypeRef = code.objects.get(codeName=imagetype['codeName'])
            if (ImageTypeRef.codeName == "ImageOption"):
                img = Image.objects.create(ImageName=imagenameo, ImageTypeCodeID=ImageTypeRef, ObjectID=opt.optionID,
                                           uploadedFile=imageurlo)
        if y['option4']['caption']['option'] == y['correctOption']:
            opt = option.objects.create(questionID=ques)
            y1 = y['option4']
            optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                        translationO=y1['caption'])
            correctOpt = optionTranslation.objects.get(optionTranslationID=optTrans.optionTranslationID, optionID=opt)
            imagenameo = y1['imageID']['ImageName']
            imageurlo = y1['imageID']['uploadedFile']
            imagetype = y1['imageID']['ImageTypeCodeID']
            ImageTypeRef = code.objects.get(codeName=imagetype['codeName'])
            if (ImageTypeRef.codeName == "ImageOption"):
                img = Image.objects.create(ImageName=imagenameo, ImageTypeCodeID=ImageTypeRef, ObjectID=opt.optionID,
                                           uploadedFile=imageurlo)

        else:
            opt = option.objects.create(questionID=ques)
            y1 = y['option4']
            optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                        translationO=y1['caption'])
            imagenameo = y1['imageID']['ImageName']
            imageurlo = y1['imageID']['uploadedFile']
            imagetype = y1['imageID']['ImageTypeCodeID']
            ImageTypeRef = code.objects.get(codeName=imagetype['codeName'])
            if (ImageTypeRef.codeName == "ImageOption"):
                img = Image.objects.create(ImageName=imagenameo, ImageTypeCodeID=ImageTypeRef, ObjectID=opt.optionID,
                                           uploadedFile=imageurlo)

        corrOpt = correctOption.objects.create(questionTranslationID=quesTrans, optionTranslationID=correctOpt,
                                               **validated_data)
        return corrOpt


class InsertTranslationSerializer(serializers.ModelSerializer):
    questionTranslationID = GetTranslatedQuestionDetail()
    optionTranslationID = GetTranslatedOptions()

    class Meta:
        model = correctOption
        fields = ('correctOptionID', 'questionTranslationID', 'optionTranslationID')

    def create(self, validated_data):
        quesTransID = validated_data.pop('questionTranslationID',None)
        quesID = quesTransID.pop('questionID')
        languageCodeID = quesTransID.pop('languageCodeID',None)
        langCodeRef = code.objects.get(codeName= languageCodeID['codeName'])
        modified_by = quesTransID.pop('modified_by',None)
        identifier = quesTransID.pop('Identifier', None)
        questionTranslations = quesTransID.pop('translation',None)
        translation = questionTranslations['translation']
        modified_on = datetime.now().date()
        quesTrans = questionTranslation.objects.create(questionID=quesID,languageCodeID=langCodeRef,
                                                       translation=translation,Identifier=identifier, modified_by=modified_by,
                                                       modified_on=modified_on)
        optionTransID = validated_data.pop('optionTranslationID',None)
        optID = optionTransID.pop('translationO')
        y = optID['translationO']
        if y['ansText'] == "":
            opt = option.objects.filter(questionID=quesID.questionID)
            serializero = GetOptions(opt, many=True)
            correctOpt = None
            if y['option1']['caption']['option'] == y['correctOption']:
                y1 = y['option1']
                opt = option.objects.get(optionID=serializero.data[0]['optionID'])
                optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                            translationO=y1['caption'])

                correctOpt = optionTranslation.objects.get(optionTranslationID=optTrans.optionTranslationID, optionID=opt)
            else:
                y1 = y['option1']
                opt = option.objects.get(optionID=serializero.data[0]['optionID'])
                optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                            translationO=y1['caption'])

            if y['option2']['caption']['option'] == y['correctOption']:
                y1 = y['option2']
                opt = option.objects.get(optionID=serializero.data[1]['optionID'])
                optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                            translationO=y1['caption'])
                correctOpt = optionTranslation.objects.get(optionTranslationID=optTrans.optionTranslationID, optionID=opt)
            else:
                y1 = y['option2']
                opt = option.objects.get(optionID=serializero.data[1]['optionID'])
                optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                            translationO=y1['caption'])

            if y['option3']['caption']['option'] == y['correctOption']:
                y1 = y['option3']
                opt = option.objects.get(optionID=serializero.data[2]['optionID'])
                optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                            translationO=y1['caption'])
                correctOpt = optionTranslation.objects.get(optionTranslationID=optTrans.optionTranslationID, optionID=opt)
            else:
                y1 = y['option3']
                opt = option.objects.get(optionID=serializero.data[2]['optionID'])
                optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                            translationO=y1['caption'])

            if y['option4']['caption']['option'] == y['correctOption']:
                y1 = y['option4']
                opt = option.objects.get(optionID=serializero.data[3]['optionID'])
                optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                            translationO=y1['caption'])
                correctOpt = optionTranslation.objects.get(optionTranslationID=optTrans.optionTranslationID,optionID=opt)
            else:
                y1 = y['option4']
                opt = option.objects.get(optionID=serializero.data[3]['optionID'])
                optTrans = optionTranslation.objects.create(optionID=opt, languageCodeID=langCodeRef,
                                                            translationO=y1['caption'])

            corrOpt = correctOption.objects.create(questionTranslationID=quesTrans, optionTranslationID=correctOpt,
                                                   **validated_data)
        else:
            corrOpt = correctOption.objects.create(questionTranslationID=quesTrans, ansText=y['ansText'],
                                                   **validated_data)
        return corrOpt

class GetAgeGroup(serializers.ModelSerializer):

    class Meta:
        model = AgeGroup
        fields = ('AgeGroupName','created_on')


class GetAgeGroupsid(serializers.ModelSerializer):

    class Meta:
        model = AgeGroup
        fields = ('AgeGroupID','AgeGroupName','created_on')

class AgeGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgeGroup
        fields = ('AgeGroupName',)

    def update(self, instance, validated_data):
        agegrp = validated_data.get('AgeGroupName')
        instance.AgeGroupName = validated_data.get('AgeGroupName',agegrp)
        instance.save()
        return instance

class GetAgeQuestion(serializers.ModelSerializer):

    AgeGroupID = GetAgeGroupsid()
    questionLevelCodeID = CodeSerializer()

    class Meta:
        model = QuestionAge
        fields = ('AgeGroupID','questionLevelCodeID')

class QuestionAgeSerializer(serializers.ModelSerializer):

    AgeGroupID = GetAgeGroupsid()
    questionLevelCodeID = CodeSerializer()
    class Meta:
        model = QuestionAge
        fields = ('AgeGroupID','questionLevelCodeID','questionID')

class QuestionAgeSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = QuestionAge
        fields=('AgeGroupID','questionLevelCodeID','questionID')

    def update(self, instance, validated_data):
        instance.AgeGroupID =  validated_data.get('AgeGroupID',instance.AgeGroupID)
        instance.questionID = validated_data.get('questionID',instance.questionID)
        instance.questionLevelCodeID = validated_data.get('questionLevelCodeID',instance.questionLevelCodeID)
        instance.save()
        return instance

class CompetitionSerializer(serializers.ModelSerializer):

    competitionType = CodeSerializer()
    class Meta:
        model=competition
        fields=('competitionID','competitionName','competitionInfo','startDate','endDate','testDuration','competitionType')

    def update(self, instance, validated_data):
        instance.competitionName = validated_data.get('competitionName',instance.competitionName)
        instance.competitionInfo = validated_data.get('competitionInfo',instance.competitionInfo)
        instance.startDate = validated_data.get('startDate',instance.startDate)
        instance.endDate = validated_data.get('endDate',instance.endDate)
        instance.testDuration = validated_data.get('testDuration', instance.testDuration)
        cmptype = validated_data.pop('competitionType')
        cmpTypeRef = code.objects.get(codeName= cmptype['codeName'])
        instance.competitionType = validated_data.get('ccompetitionType',cmpTypeRef)
        instance.save()
        return instance


class CmpSerializer(serializers.ModelSerializer):

    competitionType = CodeSerializer()
    class Meta:
        model=competition
        fields=('competitionName','startDate','competitionType')


class UpdateQuestions(serializers.ModelSerializer):
    questionTranslationID = GetTranslatedQuestion()
    optionTranslationID = GetTranslatedOptions()

    class Meta:
        model = correctOption
        fields = ('correctOptionID', 'questionTranslationID', 'optionTranslationID')

    def update(self, instance, validated_data):
        lists=[]
        lists.append(validated_data)
        quesTransID = validated_data.get('questionTranslationID', None)
        OptTransID = validated_data.get('optionTranslationID', None)
        quesID = quesTransID.pop('questionID',None)
        modified_by = quesTransID.pop('modified_by', None)
        identifier = quesTransID.pop('Identifier', None)
        domainCodeId = quesID.pop('domainCodeID', None)
        domainCodeRef = code.objects.get(codeName=domainCodeId['codeName'])
        quesTranslation = quesTransID.pop('translation',None)
        skills = quesTranslation['quescsskills'].split(',')
        cs_skills =""
        cs_skills = str(code.objects.get(codeName=skills[0]).codeID)
        for i in range(1,len(skills)):
            cs_skills = cs_skills +","+str(code.objects.get(codeName=skills[i]).codeID)
        questTransId = (instance.questionTranslationID)
        questID = (questTransId.questionID)
        questID.domainCodeID = quesID.get('domainCodeID',domainCodeRef)
        questID.cs_skills = quesID.get('cs_skills',cs_skills)
        questID.save()
        QuesAgeID = quesTranslation['quesAgeID']
        translation = quesTranslation['translation']
        competitionQuesData = QuesAgeID.get('quesData', None)
        competitionQuesDeleteData = QuesAgeID.get('DeletedQuesData', None)
        for i in range(0,len(competitionQuesDeleteData)):
            LevelID = code.objects.get(codeName=competitionQuesDeleteData[i]['quesLevel'])
            res = QuestionAge.objects.filter(questionID=questID,AgeGroupID=competitionQuesDeleteData[i]['ageID'],questionLevelCodeID=LevelID).exists()
            if res==True:
                result = QuestionAge.objects.filter(questionID=questID,AgeGroupID=competitionQuesDeleteData[i]['ageID'],questionLevelCodeID=LevelID)
                result[0].delete()
        cmpQuesFromDB = QuestionAge.objects.filter(questionID=questID)
        cnt = 0
        if len(competitionQuesData)>0:
            for i in range(0,len(competitionQuesData)):
                 LevelID = code.objects.get(codeName=competitionQuesData[i]['quesLevel'])
                 if cnt<len(cmpQuesFromDB):
                    if competitionQuesData[i]['ageID']!= cmpQuesFromDB[cnt].AgeGroupID or LevelID!=cmpQuesFromDB[cnt].questionLevelCodeID:
                        AgeGroupNameRef = AgeGroup.objects.get(AgeGroupName=competitionQuesData[i]['ageGroup'],AgeGroupID=competitionQuesData[i]['ageID'])
                        t = {"AgeGroupID":AgeGroupNameRef.AgeGroupID,
                             "questionID":questID.questionID,
                             "questionLevelCodeID":LevelID.codeID
                             }
                        inst = QuestionAgeSerializerUpdate(instance=cmpQuesFromDB[cnt],data=collections.OrderedDict(t),partial=True)
                        inst.is_valid(raise_exception=True)
                        inst.save()
                 else:
                     AgeGroupNameRef = AgeGroup.objects.get(AgeGroupName=competitionQuesData[i]['ageGroup'],AgeGroupID=competitionQuesData[i]['ageID'])
                     cmpQues = QuestionAge.objects.create(AgeGroupID=AgeGroupNameRef, questionID=questID,
                                                             questionLevelCodeID=LevelID)
                 cnt = cnt+1
        modified_on = datetime.now().date()
        questTransId.translation = quesTransID.get('translation',translation)
        questTransId.modified_by = quesTransID.get('modified_by',modified_by)
        questTransId.Identifier = quesTransID.get('Identifier',identifier)
        questTransId.modified_on = quesTransID.get('modified_on',modified_on)
        questTransId.save()
        optID = OptTransID.get('translationO')
        y = optID['translationO']
        if y['ansText'] == "":
            optList = option.objects.filter(questionID=questID.questionID)
            optTrans1 = optionTranslation.objects.filter(optionID=optList[0].optionID,languageCodeID=questTransId.languageCodeID)
            optTrans2 = optionTranslation.objects.filter(optionID=optList[1].optionID,languageCodeID=questTransId.languageCodeID)
            optTrans3 = optionTranslation.objects.filter(optionID=optList[2].optionID,languageCodeID=questTransId.languageCodeID)
            optTrans4 = optionTranslation.objects.filter(optionID=optList[3].optionID,languageCodeID=questTransId.languageCodeID)
            corropt = ""
            if y['correctOption'] == y['option1']['caption']['option']:
                z=y['option1']['caption']
                t = {"translationO":str(z)}
                inst = OptionTranslationView(instance=optTrans1[0], data=collections.OrderedDict(t), partial=True)
                inst.is_valid(raise_exception=True)
                inst.save()
                lists[0].get('optionTranslationID').update(t)
                corropt = optTrans1[0]
            else:
                z=y['option1']['caption']
                t = {"translationO":str(z)}
                inst = OptionTranslationView(instance=optTrans1[0], data=collections.OrderedDict(t), partial=True)
                inst.is_valid(raise_exception=True)
                inst.save()
            if y['correctOption'] == y['option2']['caption']['option']:
                 z=y['option2']['caption']
                 t = {"translationO":str(z)}
                 inst = OptionTranslationView(instance=optTrans2[0], data=collections.OrderedDict(t), partial=True)
                 inst.is_valid(raise_exception=True)
                 inst.save()
                 lists[0].get('optionTranslationID').update(t)
                 corropt=optTrans2[0]
            else:
                z=y['option2']['caption']
                t = {"translationO":str(z)}
                inst = OptionTranslationView(instance=optTrans2[0], data=collections.OrderedDict(t), partial=True)
                inst.is_valid(raise_exception=True)
                inst.save()
            if y['correctOption'] == y['option3']['caption']['option']:
                z=y['option3']['caption']
                t = {"translationO":str(z)}
                inst = OptionTranslationView(instance=optTrans3[0], data=collections.OrderedDict(t), partial=True)
                inst.is_valid(raise_exception=True)
                inst.save()
                lists[0].get('optionTranslationID').update(t)
                corropt=optTrans3[0]
            else:
                z=y['option3']['caption']
                t = {"translationO":str(z)}
                inst = OptionTranslationView(instance=optTrans3[0], data=collections.OrderedDict(t), partial=True)
                inst.is_valid(raise_exception=True)
                inst.save()
            if y['correctOption'] == y['option4']['caption']['option']:
                z=y['option4']['caption']
                t = {"translationO":str(z)}
                inst = OptionTranslationView(instance=optTrans4[0], data=collections.OrderedDict(t), partial=True)
                inst.is_valid(raise_exception=True)
                inst.save()
                lists[0].get('optionTranslationID').update(t)
                corropt=optTrans4[0]
            else:
                z=y['option4']['caption']
                t = {"translationO":str(z)}
                inst = OptionTranslationView(instance=optTrans4[0], data=collections.OrderedDict(t), partial=True)
                inst.is_valid(raise_exception=True)
                inst.save()
            Opt = corropt
            instance.optionTranslationID = lists[0].get('translationO',Opt)
            instance.save()
        else:
            instance.ansText = y.get('ansText',y['ansText'])
            instance.save()
        return instance

class AgeGroupClassSerializer(serializers.ModelSerializer):

    AgeGroupID = AgeGroupSerializer()
    ClassID = ClassSerializer()

    class Meta:
        model = AgeGroupClass
        fields = ('AgeGroupClassID','AgeGroupID','ClassID')


    def create(self, validated_data):
        AgeGrpData = validated_data.get('AgeGroupID')
        ClassData = validated_data.get('ClassID')
        ClassID = Class.objects.get(classNo=ClassData['classNo'])
        createdon = datetime.now().date()
        res = AgeGroup.objects.filter(AgeGroupName=AgeGrpData['AgeGroupName'],created_on=createdon).exists()
        AgeGrpIDRef=""
        if res==False:
            AgeGrpIDRef=AgeGroup.objects.create(AgeGroupName=AgeGrpData['AgeGroupName'],created_on=createdon)
        else:
            AgeGrpIDRef=AgeGroup.objects.get(AgeGroupName=AgeGrpData['AgeGroupName'],created_on=createdon)
        instance = AgeGroupClass.objects.create(AgeGroupID=AgeGrpIDRef,ClassID=ClassID)
        return instance

class AgeclassSerializer(serializers.ModelSerializer):

    AgeGroupID = GetAgeGroup()
    class Meta:
        model = AgeGroupClass
        fields = ('AgeGroupID',)

class AgeGrpClassSerializer(serializers.ModelSerializer):
    AgeGroupID = GetAgeGroupsid()
    ClassID = ClassSerializer()

    class Meta:
        model = AgeGroupClass
        fields = ('AgeGroupClassID','AgeGroupID','ClassID')

class CmpAgeSerializer(serializers.ModelSerializer):

     AgeGroupClassID = AgeclassSerializer()
     class Meta:
        model = competitionAge
        fields = ('AgeGroupClassID',)

class CompetitionAgeSerializer(serializers.ModelSerializer):

    AgeGroupClassID = AgeclassSerializer()
    competitionID = CompetitionSerializer()

    class Meta:
        model = competitionAge
        fields = ('competitionAgeID','AgeGroupClassID','competitionID','defaultBonusMarks')


    def create(self, validated_data):
        AgeClass_Data = validated_data.pop('AgeGroupClassID',None)
        Comp_Data = validated_data.pop('competitionID',None)
        ageGrpRef = AgeGroup.objects.get(AgeGroupName = AgeClass_Data['AgeGroupID']['AgeGroupName'], created_on = AgeClass_Data['AgeGroupID']['created_on'])
        AgeGrpRef = AgeGroupClass.objects.filter(AgeGroupID=ageGrpRef.AgeGroupID)
        cmptname = Comp_Data.pop('competitionType',None)
        cmpTypeRef = code.objects.get(codeName=cmptname['codeName'])
        cmpRef = competition.objects.create(competitionType=cmpTypeRef,**Comp_Data)
        cmpAge = ""
        for i in range(0,len(AgeGrpRef)):
            cmpAge = competitionAge.objects.create(AgeGroupClassID = AgeGrpRef[i],competitionID = cmpRef,**validated_data)
        return cmpAge

class CompetitionAgeOnlySerializer(serializers.ModelSerializer):

    AgeGroupClassID = AgeclassSerializer()
    competitionID = CmpSerializer()

    class Meta:
        model = competitionAge
        fields = ('competitionAgeID','AgeGroupClassID','competitionID','defaultBonusMarks')

    def create(self, validated_data):
        AgeClass_Data = validated_data.pop('AgeGroupClassID',None)
        Comp_Data = validated_data.pop('competitionID',None)
        ageGrpRef = AgeGroup.objects.get(AgeGroupName = AgeClass_Data['AgeGroupID']['AgeGroupName'], created_on = AgeClass_Data['AgeGroupID']['created_on'])
        AgeGrpRef = AgeGroupClass.objects.filter(AgeGroupID=ageGrpRef.AgeGroupID)
        cmptname = Comp_Data.pop('competitionType',None)
        cmpTypeRef = code.objects.get(codeName=cmptname['codeName'])
        CmpRef = competition.objects.get(competitionName = Comp_Data['competitionName'],startDate= Comp_Data['startDate'],competitionType=cmpTypeRef)
        cmpAge = ""
        for i in range(0,len(AgeGrpRef)):
            cmpAge = competitionAge.objects.create(AgeGroupClassID = AgeGrpRef[i],competitionID = CmpRef,**validated_data)
        return cmpAge

class studentCmpAge(serializers.ModelSerializer):
    AgeGroupClassID = AgeGrpClassSerializer()
    competitionID = CmpSerializer()

    class Meta:
        model = competitionAge
        fields = ('competitionAgeID','AgeGroupClassID','competitionID','defaultBonusMarks')


class CompetitionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = competitionQuestion
        fields = ('competitionQuestionID','competitionAgeID','questionID','questionLevelCodeID')

    def create(self, validated_data):
        cmpques = competitionQuestion.objects.create(**validated_data)
        return cmpques

class CmpQuesSerializer(serializers.ModelSerializer):

    questionLevelCodeID = CodeSerializer()
    class Meta:
         model = competitionQuestion
         fields = ('competitionQuestionID','competitionAgeID','questionID','questionLevelCodeID')


class CmpQuesGetAllSerializer(serializers.ModelSerializer):
    competitionAgeID=CompetitionAgeSerializer()
    questionLevelCodeID = CodeSerializer()
    class Meta:
         model = competitionQuestion
         fields = ('competitionQuestionID','competitionAgeID','questionID','questionLevelCodeID')


class MarkingSchemeSerializer(serializers.ModelSerializer):
    questionLevelCodeID = CodeSerializer()

    class Meta:
        model = competition_MarkScheme
        fields = ('competitionAgeID','questionLevelCodeID','correctMarks','incorrectMarks')

    def update(self, instance, validated_data):
        level = validated_data.pop('questionLevelCodeID')
        leveCodeRef = code.objects.get(codeName=level['codeName'])
        instance.competitionAgeID = validated_data.get('competitionAgeID',instance.competitionAgeID)
        instance.questionLevelCodeID = validated_data.get('questionLevelCodeID',leveCodeRef)
        instance.correctMarks = validated_data.get('correctMarks',instance.correctMarks)
        instance.incorrectMarks = validated_data.get('incorrectMarks',instance.incorrectMarks)
        instance.save()
        return instance

class studentEnrollmentSerializer(serializers.ModelSerializer):
    schoolClassID= SchoolClassSerializers()
    userID= UserSerializer()
    languageCodeID=CodeSerializer()
    competitionAgeID= studentCmpAge()
    class Meta:
        model= studentEnrollment
        fields =('studentEnrollmentID','timeTaken','score','additionalTime','languageCodeID','competitionAgeID','schoolClassID','userID','bonusMarks')


#user portal

class CmpEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = studentEnrollment
        fields = ( 'competitionAgeID','languageCodeID','userID','schoolClassID','timeTaken','score','bonusMarks')

class studentEnrollmentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = studentEnrollment
        fields = '__all__'

class StudentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = studentResponse
        fields = ( 'competitionQuestionID','studentEnrollmentID','optionTranslationID','time','ansText')
