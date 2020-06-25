from rest_framework import serializers
from .models import *
from com.serializers import *
from com.models import *

class GetQuestion(serializers.ModelSerializer):
    countryID = CountrySerializer()
    domainCodeID = CodeSerializer()
    questionTypeCodeID = CodeSerializer()

    class Meta:
        model = question
        fields = ('questionID','countryID','domainCodeID','questionTypeCodeID','cs_skills')

class GetOptions(serializers.ModelSerializer):

    class Meta:
        model = option
        fields = ('questionID','optionID')

class GetOptionsID(serializers.ModelSerializer):

    class Meta:
        model = option
        fields = ('optionID',)

class GetTranslatedQuestion(serializers.ModelSerializer):
    questionID = GetQuestion()
    languageCodeID = CodeSerializer()
    translation = serializers.JSONField()

    class Meta:
        model = questionTranslation
        fields = ('questionTranslationID', 'questionID', 'languageCodeID', 'translation','modified_by','Identifier')

class GetTranslatedQuestionDetail(serializers.ModelSerializer):
    languageCodeID = CodeSerializer()
    translation = serializers.JSONField()

    class Meta:
        model = questionTranslation
        fields = ('questionTranslationID', 'questionID', 'languageCodeID', 'translation','Identifier','modified_by','modified_on')

class GetImages(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('ImageID','uploadedFile','ObjectID')

class GetTranslatedOptions(serializers.ModelSerializer):

    languageCodeID = CodeSerializer()
    translationO = serializers.JSONField()

    class Meta:
        model = optionTranslation
        fields = ( 'languageCodeID', 'translationO')

class GetAllTranslatedOptions(serializers.ModelSerializer):
    optionID = GetOptions()
    languageCodeID = CodeSerializer()
    translationO = serializers.JSONField()

    class Meta:
        model = optionTranslation
        fields = ( 'languageCodeID','translationO','optionID','optionTranslationID')


class GetCorrectOption(serializers.ModelSerializer):
    questionTranslationID = GetTranslatedQuestion()
    optionTranslationID = GetAllTranslatedOptions()

    class Meta:
        model = correctOption
        fields = ('questionTranslationID','optionTranslationID','ansText')


class GetQuestionSkills(serializers.ModelSerializer):
    class Meta:
        model = question
        fields = ('cs_skills',)

class OptionTranslationView(serializers.ModelSerializer):
    class Meta:
        model = optionTranslation
        fields = ('translationO',)

    def update(self, instance, validated_data):
        val = eval(validated_data.get('translationO'))
        instance.translationO = eval(validated_data.get('translationO',val))
        instance.save()
        return instance


#user Portal

class CorrectOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = correctOption
        fields = '__all__'

class quesTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = questionTranslation
        fields = '__all__'


class OptionTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = optionTranslation
        fields = '__all__'
