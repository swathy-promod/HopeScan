from django.urls import path
from .import views
app_name = 'Administrator'

urlpatterns = [
    path('District/',views.district, name='District'),
    path('Category/',views.category, name='Category'),
    path('SubCategory/',views.subcategory, name='SubCategory'),
    path('Place/',views.place, name='Place'),
    path('AdminRegistration/',views.adminregistration, name='AdminRegistration'),
    path("Districtdelete/<int:id>/",views.districtdelete,name="Districtdelete"),
    path("Categorydelete/<int:id>/",views.categorydelete,name="Categorydelete"),
    path('Adminregistrationdelete/<int:id>/',views.adminregistrationdelete,name='Adminregistrationdelete'),
    path("districtedit/<int:id>/",views.districtedit,name="districtedit"),
    path("categoryedit/<int:id>/",views.categoryedit,name="categoryedit"),
    path("adminregistrationedit/<int:id>/",views.adminregistrationedit,name="Adminregistrationedit"),
    path("Subcategory/",views.subcategory,name='Subcategory'),
    path('Deletesubcategory/<int:id>/',views.deletesubcategory,name='Deletesubcategory'),
    path('Placeedit/<int:id>/',views.placeedit,name='Placeedit'),
    path('editsubcategory/<int:id>/',views.editsubcategory,name='editsubcategory'),
    path('userlist/',views.userlist,name="userlist"),
    path('Accept/<int:id>/',views.acceptuser, name='Accept'),
    path('Reject/<int:id>/',views.rejectuser, name="Reject"),
    path('ViewComplaint/',views.viewcomplaint, name="ViewComplaint"),
    path('reply/<int:cid>/',views.reply,name="reply"),
    path("Viewfeedback/",views.viewfeedback,name='Viewfeedback'),
    path('Doctorlist/',views.doctorlist,name="Doctorlist"),
    path('DoctorAccept/<int:id>/',views.acceptdoctor, name='DoctorAccept'),
    path('DoctorReject/<int:id>/',views.rejectdoctor, name='DoctorReject'),
    path("HomePage/",views.homepage,name='HomePage'),
    path("Logout/",views.logout,name="Logout"),
]

