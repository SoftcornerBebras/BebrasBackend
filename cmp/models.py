from django.db import models
from com.models import *
from ques.models import *
from usr.models import *
import datetime

class competition(models.Model):
    competitionID = models.AutoField(db_column='competitionID', primary_key=True)
    competitionName = models.CharField(max_length=50, null=False)
    competitionInfo = models.CharField(max_length=100, null=False)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    testDuration = models.TimeField()
    competitionType = models.ForeignKey(code, db_column='competitionType', default=111002,to_field='codeID', on_delete=models.CASCADE)

class AgeGroup(models.Model):
    AgeGroupID = models.AutoField(db_column='AgeGroupID', primary_key=True)
    AgeGroupName = models.CharField(db_column='AgeGroupName',max_length=30)
    created_on = models.DateField()

class AgeGroupClass(models.Model):
    AgeGroupClassID = models.AutoField(db_column='AgeGroupClassID', primary_key=True)
    AgeGroupID = models.ForeignKey(AgeGroup, db_column='AgeGroupID',null=True, to_field='AgeGroupID',
                                      on_delete=models.CASCADE)
    ClassID = models.ForeignKey(Class, db_column='classID',null=True, to_field='classID',
                                      on_delete=models.CASCADE)

class competitionAge(models.Model):
    competitionAgeID = models.AutoField(db_column='competitionAgeID', primary_key=True)
    AgeGroupClassID =  models.ForeignKey(AgeGroupClass, db_column='AgeGroupClassID',null=True, to_field='AgeGroupClassID',
                                      on_delete=models.CASCADE)
    competitionID = models.ForeignKey(competition, db_column='competitionID',null=True, to_field='competitionID',
                                      on_delete=models.CASCADE)
    defaultBonusMarks = models.IntegerField()


class QuestionAge(models.Model):
    QuestionAgeID = models.AutoField(db_column='QuestionAgeID', primary_key=True)
    AgeGroupID = models.ForeignKey(AgeGroup, db_column='AgeGroupID',null=True, to_field='AgeGroupID',
                                      on_delete=models.CASCADE)
    questionLevelCodeID = models.ForeignKey(code,related_name='questionLevelCode', db_column='questionLevelCodeID', to_field='codeID', on_delete=models.CASCADE)
    questionID = models.ForeignKey(question, db_column='questionID', to_field='questionID', on_delete=models.CASCADE)

class competitionQuestion(models.Model):
    competitionQuestionID = models.AutoField(db_column='competitionQuestionID', primary_key=True)
    competitionAgeID = models.ForeignKey(competitionAge, db_column='competitionAgeID', to_field='competitionAgeID',
                                         on_delete=models.CASCADE)
    questionID = models.ForeignKey(question, db_column='questionID', to_field='questionID', on_delete=models.CASCADE)
    questionLevelCodeID = models.ForeignKey(code,related_name='questionLevelCodeID',default=107001, db_column='questionLevelCodeID', to_field='codeID', on_delete=models.CASCADE)

class competition_MarkScheme(models.Model):
    competition_MarkSchemeID = models.AutoField(db_column='competition_MarkSchemeID', primary_key=True)
    competitionAgeID = models.ForeignKey(competitionAge, db_column='competitionAgeID', to_field='competitionAgeID',
                                         on_delete=models.CASCADE)
    questionLevelCodeID = models.ForeignKey(code,db_column='questionLevelCodeID', to_field='codeID', on_delete=models.CASCADE)
    correctMarks = models.IntegerField(null=False)
    incorrectMarks = models.IntegerField(null=False)


class studentEnrollment(models.Model):
    studentEnrollmentID = models.AutoField(db_column='studentEnrollmentID', primary_key=True)
    competitionAgeID = models.ForeignKey(competitionAge, db_column='competitionAgeID', to_field='competitionAgeID',
                                         on_delete=models.CASCADE)
    languageCodeID = models.ForeignKey(code, db_column='languageCodeID', to_field='codeID', on_delete=models.CASCADE)
    timeTaken = models.TimeField(null=False)
    score = models.IntegerField(null=False)
    schoolClassID=models.ForeignKey(schoolClass,db_column='schoolClassID',default=1,to_field='schoolClassID', on_delete=models.CASCADE)
    userID = models.ForeignKey(User, db_column='userID', to_field='userID', on_delete=models.CASCADE)
    additionalTime=models.TimeField(null=True)
    bonusMarks = models.IntegerField()

class studentResponse(models.Model):
    studentResponseID = models.AutoField(db_column='studentResponseID', primary_key=True)
    competitionQuestionID = models.ForeignKey(competitionQuestion, to_field='competitionQuestionID',
                                              db_column='competitionQuestionID', on_delete=models.CASCADE)
    studentEnrollmentID = models.ForeignKey(studentEnrollment, to_field='studentEnrollmentID',
                                            db_column='studentEnrollmentID', on_delete=models.CASCADE)
    optionTranslationID = models.ForeignKey(optionTranslation, default=1,null=True,to_field='optionTranslationID', db_column='optionTranslationID', on_delete=models.CASCADE)
    ansText = models.CharField(max_length=20,null=True)
    time = models.FloatField()
