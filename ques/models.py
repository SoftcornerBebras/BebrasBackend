from django.db import models
import jsonfield
from django.utils import timezone
from com.models import *
import datetime

class question(models.Model):
    questionID=models.AutoField(db_column='questionID',primary_key=True)
    countryID=models.ForeignKey(Countries,db_column='countryID',to_field='countryID',on_delete=models.CASCADE)
    domainCodeID=models.ForeignKey(code,related_name='domainCode',db_column='domainCodeID',to_field='codeID',on_delete=models.CASCADE)
    questionTypeCodeID=models.ForeignKey(code,related_name='questionTypeCode',db_column='questionTypeCodeID',to_field='codeID',on_delete=models.CASCADE)
    cs_skills = models.CharField(max_length=50, default='default value')

class option(models.Model):
    optionID=models.AutoField(db_column='optionID',primary_key=True)
    questionID=models.ForeignKey(question,db_column='questionID',to_field='questionID',on_delete=models.CASCADE)


class questionTranslation(models.Model):
    questionTranslationID=models.AutoField(db_column='questionTranslationID',primary_key=True)
    questionID=models.ForeignKey(question,db_column='questionID',to_field='questionID',on_delete=models.CASCADE)
    languageCodeID=models.ForeignKey(code,db_column='languageCodeID',to_field='codeID',on_delete=models.CASCADE)
    translation=jsonfield.JSONField()
    modified_on = models.DateTimeField()
    modified_by = models.CharField(max_length=50, default='default value')
    Identifier = models.CharField(max_length=50)

class optionTranslation(models.Model):
    optionTranslationID=models.AutoField(db_column='optionTranslationID',primary_key=True)
    optionID=models.ForeignKey(option,db_column='optionID',to_field='optionID',on_delete=models.CASCADE)
    languageCodeID=models.ForeignKey(code,db_column='languageCodeID',to_field='codeID',on_delete=models.CASCADE)
    translationO=jsonfield.JSONField()

class correctOption(models.Model):
    correctOptionID=models.AutoField(db_column='correctOptionID',primary_key=True)
    questionTranslationID=models.ForeignKey(questionTranslation,db_column='questionTranslationID',on_delete=models.CASCADE,to_field='questionTranslationID')
    optionTranslationID=models.ForeignKey(optionTranslation,db_column='optionTranslationID',to_field='optionTranslationID',on_delete=models.CASCADE,null=True)
    ansText = models.CharField(max_length=20,null=True)

class Image(models.Model):
    ImageID = models.AutoField(db_column='ImageID',primary_key=True)
    ImageName = models.CharField(db_column='ImageName',max_length=50)
    ImageTypeCodeID = models.ForeignKey(code,db_column='ImageTypeCodeID',to_field='codeID',on_delete=models.CASCADE)
    ObjectID = models.IntegerField(db_column='ObjectID')
    uploadedFile = models.CharField(db_column='uploadedFile',max_length=128)
