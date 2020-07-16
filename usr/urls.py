"""bebras14 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.urls import  include
from . import views
from .api import *
from knox import views as knox_views
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('login/',views.LoginView.as_view()),
    path('logout/',views.LogoutView.as_view()),
    re_path('updateUser/(?P<userRoleID>\d+)/$',views.UpdateView.as_view()),
    re_path('updateProfile/(?P<userID>\d+)/$',views.UpdateProfileView.as_view()),
    re_path('getProfile/(?P<loginID>[\w.@+-]+)/$',views.SingleUserProfile.as_view()),
    path('getAdmins/',views.UserAdminView.as_view()),
    path('viewUsers/',views.UserPageView.as_view()),
    path('insertUser/',views.InsertUserView.as_view()),
    path('reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',views.ConfirmResetPasswordView.as_view(),name='reset_password_confirm'),
    path('reset_password/',views.ResetPasswordView.as_view()),
    path('roleList/',views.RoleListView.as_view()),
    path('roleListAdd/',views.RoleListAdd.as_view()),
    path('changePassword/',views.ChangePasswordView.as_view()),
    path('getGender/',views.GetGenderView.as_view()),
    re_path('userProfileUsers/(?P<loginID>[\w.@+-]+)/$',views.UserPTimeline.as_view()),
    re_path('getRegisteredBy/(?P<loginID>[\w.@+-]+)/$',views.GetRegisteredBy.as_view()),
    re_path('viewUserRoleLocation/(?P<schoolID>\d+)&(?P<type>[\w.@+-]+)/$', views.GetUserRoleLocationPageView.as_view()),
    re_path('getUserRoleLocation/(?P<schoolID>\d+)&(?P<type>[\w.@+-]+)/$', views.GetUserRoleLocationView.as_view()),
    path('getUserSearch/',views.UserSearch.as_view()),

    #user portal
    path('registerteacher', TeacherRegisterAPI.as_view()),
    path('registerschool', SchoolRegisterAPI.as_view()),
    path('login-page', LoginAPI.as_view()),
    path('teacherregisterteacher', TeacherRegistrationAPI.as_view()),
    path('registerstudent', StudentRegisterAPI.as_view()),
    path('bulkregisterstudent', StudentBulkRegisterAPI.as_view()),
    path('bulkstudentenrollment',StudentBulkCompetitionRegisterAPI.as_view()),
    path('currentuserdetail', UserAPI.as_view()),
    path('getuserdataexcel', UserExcelAPI.as_view()),
    path('ResetPasswordView', ResetPasswordView.as_view()),
    path('ConfirmResetPasswordView', ConfirmResetPasswordView.as_view()),
    path('ContactUsMail', ContactUsMailApi.as_view()),
    path('', include('knox.urls')),
    path('Alluserresult',     AllUserResultViewAPI.as_view()),
    path('userresult',     UserResultViewAPI.as_view()),
    path('usersenrolled',     AllStudentsEnrolledViewAPI.as_view()),
    path('userdata', UserViewAPI.as_view()),
    path('logout-page', knox_views.LogoutView.as_view(), name='knox_logout')
]
