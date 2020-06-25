from django.contrib import admin
from django.urls import path,re_path
from . import views as cviews
from rest_framework.schemas import get_schema_view
from .api import *

urlpatterns = [
    re_path('updateSchools/(?P<schoolID>\d+)/$',cviews.UpdateSchoolView.as_view()),
    path('viewSchools/',cviews.SchoolPageView.as_view()),
    path('getDistrict/',cviews.GetDistrictView.as_view()),
    path('getState/',cviews.GetStateView.as_view()),
    path('getCountry/',cviews.GetCountryView.as_view()),
    path('getClasses/',cviews.GetClassView.as_view()),
    path('getQuestionType/',cviews.GetQuestionTypeView.as_view()),
    path('getLanguage/',cviews.GetLanguageView.as_view()),
    path('getQuestionLevel/',cviews.GetQuestionLevelView.as_view()),
    path('getDomain/',cviews.GetDomainView.as_view()),
    path('getSkills/',cviews.GetSkillsView.as_view()),
    path('getCmpTypes/',cviews.GetCmpTypes.as_view()),
    path('getAddress/',cviews.GetAddressView.as_view()),
    path('insertLanguage/',cviews.InsertNewLanguage.as_view()),
    path('insertDomain/',cviews.InsertNewDomain.as_view()),
    path('insertLevel/',cviews.InsertNewLevel.as_view()),
    path('insertSkill/',cviews.InsertNewSkill.as_view()),
    path('insertSchoolGrps/',cviews.InsertNewSchoolGroup.as_view()),
    path('getSchool/',cviews.GetSchoolView.as_view()),
    path('getSchoolList/',cviews.GetSchoolList.as_view()),
    re_path('getSchoolWiseClasses/(?P<schoolID>\d+)/$',cviews.GetSchoolWiseClasses.as_view()),
    re_path('getStateCountryWise/(?P<countryID>\d+)/$',cviews.GetStateCountryWise.as_view()),
    re_path('getDistrictStateWise/(?P<stateID>\d+)/$',cviews.GetDistrictStateWise.as_view()),
    path('getSchoolGroups/',cviews.GetGroup.as_view()),
    path('getSchoolTypes/',cviews.GetSchoolType.as_view()),
    re_path('userProfileSchool/(?P<loginID>[\w.@+-]+)/$',cviews.SchoolPTimeline.as_view()),

    #userportal
    path('cmpnames', CompetitionNameAPI.as_view()),
    path('cmpnamesforcertificate', CompetitionNameForCertificatesAPI.as_view()),
    path('countrynames', CountryNameAPI.as_view()),
    path('schoolnames', SchoolNameAPI.as_view()),
    path('schoolclasses', SchoolClassesAPI.as_view()),
    path('statenames', StateNameAPI.as_view()),
    path('districtnames', DistrictNameAPI.as_view()),
    path('schoolGroupnames', SchoolGroupAPI.as_view()),
    path('AgeGroupnames', AgeGroupNameAPI.as_view()),
    path('getschooltypenames', SchoolTypeName.as_view()),
    path('getgendernames', GenderName.as_view()),

]
