from django.urls import path
from Doctor import views
app_name = "Doctor"

urlpatterns = [
    path("MyProfileDoctor/",views.myprofiledoctor,name="MyProfileDoctor"),
    path("EditProfileDoctor/",views.editprofiledoctor,name="EditProfileDoctor"),
    path("ChangePasswordDoctor/",views.changepassworddoctor,name="ChangePasswordDoctor"),
    path("Homepage/",views.homepage,name="Homepage"),
    path("Slot/",views.slot,name="Slot"),
    path('Deleteslot/<int:id>/',views.deleteslot,name='Deleteslot'),
    path('ViewAppointment/',views.viewappointment,name="ViewAppointment"),
    path('Appointmentaccept/<int:id>/',views.appointmentaccept,name="Appointmentaccept"),
    path('Appointmentreject/<int:id>/',views.appointmentreject,name="Appointmentreject"),
    path('Amount/<int:aid>',views.amount,name="Amount"),

    path('Imagepredict/',views.Imagepredict,name="Imagepredict"),



]