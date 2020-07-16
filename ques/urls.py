from django.contrib import admin
from django.urls import path,re_path
from . import views as qviews
from rest_framework.schemas import get_schema_view


urlpatterns = [
     re_path('userProfileQues/(?P<loginID>[\w.@+-]+)/$',qviews.UserProfileQuesTimeline.as_view()),
     path('viewQuestions/',qviews.QuestionPageView.as_view()),
     re_path('getOptions/(?P<limit1>\d+)&(?P<limit2>\d+)/$',qviews.OptionView.as_view()),
     re_path('getTranslations/(?P<questionID>\d+)/$',qviews.ViewTraslations.as_view()),
     re_path('getImages/(?P<ObjectID>\d+)/$',qviews.ViewImage.as_view()),
     re_path('getQuesSkills/(?P<questionID>\d+)/$',qviews.ViewQuestionSkills.as_view()),
     path('editDbQues/',qviews.EditPreviousQuestion.as_view()),
     path('getQuesSearch/',qviews.QuestionSearch.as_view()),
]
