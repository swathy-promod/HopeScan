from django.shortcuts import render,redirect
from Administrator.models import*
from Guest.models import*
from User.models import*

# Create your views here.

def logout(request):
    del request.session['aid']
    return redirect("Guest:Login")

def district(request):
    if 'aid' in request.session:
        district_data=tbl_district.objects.all()    
        if request.method=='POST':
            dist=request.POST.get('txt_district')
            tbl_district.objects.create(district_name=dist)
            return redirect("Administrator:District")
        else:
            return render(request, 'Administrator/District.html',{'district':district_data})
    else:
        return redirect("Guest:Login")
    
def districtdelete(request,id):
    tbl_district.objects.get(id=id).delete()
    return redirect("Administrator:District")

def districtedit(request,id):
    editdistrict=tbl_district.objects.get(id=id)
    if request.method=='POST':
        name=request.POST.get('txt_district')
        editdistrict.district_name=name
        editdistrict.save()
        return redirect("Administrator:District")
    else:
        return render(request,"Administrator/District.html",{'data':editdistrict})

def categorydelete(request,id):
    tbl_category.objects.get(id=id).delete()
    return redirect("Administrator:Category")   

def categoryedit(request,id):
    categoryedit=tbl_category.objects.get(id=id)
    if request.method=='POST':
        name=request.POST.get('txt_category')
        categoryedit.category_name=name
        categoryedit.save()
        return redirect("Administrator:Category")
    else:
        return render(request,"Administrator/Category.html",{'data':categoryedit})

def category(request):
    category_data=tbl_category.objects.all()
    if request.method=='POST':
        cat=request.POST.get('txt_category')
        tbl_category.objects.create(category_name=cat)
        return redirect("Administrator:Category")
    else:
        return render(request, 'Administrator/Category.html',{'category':category_data})
    
def subcategory(request):
    category_data=tbl_category.objects.all() 
    subcategory_data=tbl_subcategory.objects.all()   
    if request.method=='POST':
        subname=request.POST.get('txt_subcategory')
        subsel=request.POST.get('sel_category')
        category_data=tbl_category.objects.get(id=subsel)
        tbl_subcategory.objects.create(
            subcategory_name=subname,
            category=category_data      
            
            )
        return redirect("Administrator:Subcategory")
    else:
        return render(request, 'Administrator/SubCategory.html',{'Subcategory':subcategory_data,'Category':category_data})

def place(request):
    district_data=tbl_district.objects.all()
    place_data=tbl_place.objects.all()    
    if request.method=='POST':  
        place=request.POST.get('txt_place')
        district_id=request.POST.get("select_district")
        district_obj=tbl_district.objects.get(id=district_id)
        tbl_place.objects.create(
            place_name=place,
            district=district_obj)
        return redirect("Administrator:Place")
    else:
        return render(request, 'Administrator/Place.html',{'place':place_data,'district':district_data})
    
def placeedit(request,id):
    district_data=tbl_district.objects.all()
    placeedit=tbl_place.objects.get(id=id)
    if request.method=='POST':
        name=request.POST.get('txt_place')
        placeedit.place_name=name
        district_id=request.POST.get("select_district")
        district_obj=tbl_district.objects.get(id=district_id)
        placeedit.district=district_obj
        placeedit.save()
        
    
        return redirect("Administrator:Place")
    else:
        return render(request, 'Administrator/Place.html',{'editdata':placeedit,'district':district_data})

def adminregistrationdelete(request,id):
    tbl_adminregistration.objects.get(id=id).delete()
    return redirect("Administrator:AdminRegistration")

def adminregistrationedit(request,id):
    adminregistrationedit=tbl_adminregistration.objects.get(id=id)
    if request.method=='POST':
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_email')
        password=request.POST.get('txt_password')
        adminregistrationedit.adminregistration_name=name
        adminregistrationedit.adminregistration_email=email
        adminregistrationedit.adminregistration_password=password
        adminregistrationedit.save()
        return redirect("Administrator:AdminRegistration")
    else:
        return render(request,"Administrator/AdminRegistration.html",{'data':adminregistrationedit})    

def adminregistration(request):
        adminregistration_data=tbl_adminregistration.objects.all()
        if request.method=="POST":
            name=request.POST.get('txt_name') 
            email=request.POST.get('txt_email')
            password=request.POST.get('txt_password')
            tbl_adminregistration.objects.create(userregistration_name=name,userregistration_email=email,userregistration_password=password)
            return redirect("Administrator:AdminRegistration")
        else:
            return render(request, 'Administrator/AdminRegistration.html',{'adminregistration':adminregistration_data})
    
def deletesubcategory(request,id):
    tbl_subcategory.objects.get(id=id).delete()
    return redirect("Administrator:Subcategory")

def editsubcategory(request,id):
    subcategory_data=tbl_subcategory.objects.get(id=id)
    category_data=tbl_category.objects.all()
    if request.method=='POST':
        subname=request.POST.get('txt_subcategory')
        subsel=request.POST.get('sel_category')
        category_data=tbl_category.objects.get(id=subsel)
        subcategory_data.subcategory_name=subname
        subcategory_data.category=category_data
        subcategory_data.save()
        return redirect("Administrator:Subcategory")
    else:
        return render(request, 'Administrator/SubCategory.html',{'editdata':subcategory_data,'Category':category_data})
    


def userlist(request):
    userlist_data=tbl_userregistration.objects.all()
    return render(request,"Administrator/UserList.html",{'userlist':userlist_data})

def acceptuser(request,id):
    userlist_data=tbl_userregistration.objects.get(id=id)
    userlist_data.user_status=1
    userlist_data.save()
    return render(request,"Administrator/Userlist.html",{'msg':"Accepted"})

def rejectuser(request,id):
    userlist_data=tbl_userregistration.objects.get(id=id)
    userlist_data.user_status=2
    userlist_data.save()
    return render(request,"Administrator/Userlist.html",{'msg':"Rejected"})

def viewcomplaint(request):
    complaintdata=tbl_complaint.objects.all()
    return render(request,'Administrator/ViewComplaint.html',{'complaintdata':complaintdata})

def reply(request,cid):
    compdata=tbl_complaint.objects.get(id=cid)
    if request.method=='POST':
        reply=request.POST.get('txt_reply')
        compdata.complaint_reply=reply
        compdata.complaint_status=1
        compdata.save()
        return render(request,'Administrator/Reply.html',{'msg':"Replied"})
    else:
        return render(request,'Administrator/Reply.html')
    
def viewfeedback(request):
    viewfeedbackdata=tbl_feedback.objects.all()
    return render(request,'Administrator/ViewFeedback.html',{'viewfeedbackdata':viewfeedbackdata})

def doctorlist(request):
    doctordata=tbl_doctorregistration.objects.all()
    return render(request,'Administrator/Doctorlist.html',{'doctorlist':doctordata})

def acceptdoctor(request,id):
    doctorlist_data=tbl_doctorregistration.objects.get(id=id)
    doctorlist_data.doctor_status=1
    doctorlist_data.save()
    return render(request,"Administrator/doctorlist.html",{'msg':"Accepted"})

def rejectdoctor(request,id):
    doctorlist_data=tbl_doctorregistration.objects.get(id=id)
    doctorlist_data.user_status=2
    doctorlist_data.save()
    return render(request,"Administrator/doctorlist.html",{'msg':"Rejected"})

def homepage(request):
    return render(request,'Administrator/HomePage.html')