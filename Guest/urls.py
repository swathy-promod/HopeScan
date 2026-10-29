from django.urls import path
from .import views
app_name = 'Guest'
urlpatterns = [
    path('Login/', views.login, name='Login'),
    path('UserRegistration/', views.userregistration, name='UserRegistration'),
    path('ajaxplace/',views.ajaxplace,name='ajaxplace'),
    path('DoctorRegistration/',views.doctorregistration,name="DoctorRegistration"),
    path('',views.index,name="index"),
    path('ForgotPassword/',views.forgotpassword,name='forgotpassword'),
    path('OTP/',views.otp,name='otp'),
    path('NewPassword/',views.newpass,name='newpass'),  

]