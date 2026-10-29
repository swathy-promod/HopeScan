from django.urls import path
from User import views
app_name = "User"

urlpatterns =[
    path('Homepage/',views.Homepage,name="Homepage"),
    path('Myprofile/',views.Myprofile,name="Myprofile"),
    path('EditProfile/',views.editprofile,name='EditProfile'),
    path('ChangePassword/',views.changepassword,name='ChangePassword'),
    path('Complaint/',views.complaint,name='Complaint'),
    path('Feedback/',views.feedback,name="Feedback"),
    path('ViewsDoctor/',views.viewsdoctor,name="ViewsDoctor"),
    path('Bookappointment/<int:id>/',views.bookappointment,name="Bookappointment"),
    path('MyAppointment/',views.myappointment,name="MyAppointment"), 
    path('Payment/<int:id>/',views.payment,name="Payment"), 

    path('Imagepredict/',views.Imagepredict,name="Imagepredict"),



]