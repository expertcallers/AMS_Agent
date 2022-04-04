from django.urls import path
from .views import *

urlpatterns = [
    # Login
    path('',loginPage),
    path('login/',loginAndRedirect),
    path('login',loginAndRedirect),
    path('logout',logoutView),
    path('change-password',change_password),
    path('upload-image',uploadImageToDB),
    path('agent-dashboard',agentDashBoard),
    path('ams-agent-settings',agentSettings),
    path('ams-apply_leave',applyLeave),
    path('add-attendance', addAttendance),
]