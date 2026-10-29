from django.shortcuts import render,redirect
from Guest.models import *
from Administrator.models import *
import random
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def login(request):
    if request.method=="POST":
        email = request.POST.get("username")
        password=request.POST.get("password")

        usercount = tbl_userregistration.objects.filter(userregistration_email=email,userregistration_password=password).count()
        admincount = tbl_adminregistration.objects.filter(adminregistration_email=email,adminregistration_password=password).count()
        doctorcount=tbl_doctorregistration.objects.filter(doctorregistration_email=email,doctorregistration_password=password).count()
        if usercount > 0:
            userdata = tbl_userregistration.objects.get(userregistration_email=email,userregistration_password=password)
            if userdata.user_status==1:
                 request.session['uid']=userdata.id
            elif userdata.user_status==2:
                return render(request,"Guest/Login.html",{'msg':"VERIFICATION REJECTED"})
            elif userdata.user_status==0:
                 return render(request,"Guest/Login.html",{'msg':"Verification pending"})            
            request.session['uid'] = userdata.id
            return redirect("User:Homepage")
        
        elif admincount > 0:
             admindata = tbl_adminregistration.objects.get(adminregistration_email=email,adminregistration_password=password)
             request.session['aid'] = admindata.id
             return redirect("Administrator:HomePage")
        
        elif doctorcount > 0:
            doctordata = tbl_doctorregistration.objects.get(doctorregistration_email=email,doctorregistration_password=password)
            if doctordata.doctor_status==1:
                request.session['did']=doctordata.id
                return redirect("Doctor:Homepage")
            elif doctordata.doctor_status==2:
                return render(request,"Guest/Login.html",{'msg':"VERIFICATION REJECTED"})
            elif doctordata.doctor_status==0:
                return render(request,"Guest/Login.html",{'msg':"Verification pending"})            
        else:
            return render(request,"Guest/Login.html",{'msg':"Invalid Email Or Password"})
    else:
        return render(request, 'Guest/Login.html')



def userregistration(request):
        userregistration_data=tbl_userregistration.objects.all()
        district_data=tbl_district.objects.all()
        place_data=tbl_place.objects.all()    
        if request.method=="POST":
            name=request.POST.get('txt_name') 
            email=request.POST.get('txt_email')
            contact=request.POST.get('txt_contact')
            address=request.POST.get('txt_address')
            gender=request.POST.get('gender')
            dateofbirth=request.POST.get('txt_dob')
            district_id=request.POST.get("select_district")
            district_obj=tbl_district.objects.get(id=district_id)
            place_id=request.POST.get("place_name")
            place_obj=tbl_place.objects.get(id=place_id)
            photo=request.FILES.get('txt_photo')
            password=request.POST.get('txt_pass')
            tbl_userregistration.objects.create(userregistration_name=name,userregistration_email=email,userregistration_contact=contact,
                                                userregistration_address=address,userregistration_gender=gender,userregistration_dateofbirth=dateofbirth,
                                                userregistration_place=place_obj,userregistration_photo=photo,userregistration_password=password)
            return redirect("Guest:UserRegistration")
        else:
            return render(request,'Guest/UserRegistration.html',{'userregistration':userregistration_data,'district':district_data,'place':place_data})

def ajaxplace(request):
     did=request.GET.get('did')
     place=tbl_place.objects.filter(district=did)
     return render(request,'Guest/Ajaxplace.html',{'place':place})

def doctorregistration(request):
    doctorregistration_data=tbl_doctorregistration.objects.all()
    district_data=tbl_district.objects.all()
    place_data=tbl_place.objects.all()    
    if request.method=="POST":
        name=request.POST.get('txt_name') 
        email=request.POST.get('txt_email')
        contact=request.POST.get('txt_contact')
        address=request.POST.get('txt_address')
        gender=request.POST.get('gender')
        district_id=request.POST.get("select_district")
        district_obj=tbl_district.objects.get(id=district_id)
        place_id=request.POST.get("place_name")
        place_obj=tbl_place.objects.get(id=place_id)
        photo=request.FILES.get('txt_photo1')
        proof=request.FILES.get('txt_photo2')
        password=request.POST.get('txt_pass')
        exp=request.POST.get('txt_exp')
        tbl_doctorregistration.objects.create(doctorregistration_name=name,doctorregistration_email=email,doctorregistration_contact=contact,
                                        doctorregistration_address=address,doctorregistration_gender=gender,doctorregistration_place=place_obj,
                                        doctorregistration_photo=photo,doctorregistration_password=password,doctorregistration_proof=proof,
                                        doctorregistration_exp=exp)
        return redirect("Guest:DoctorRegistration")
    else:
        return render(request,'Guest/DoctorRegistration.html',{'doctorregistration':doctorregistration_data,'district':district_data,'place':place_data})

def index(request):
    return render(request,'Guest/index.html') 

def forgotpassword(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        user = tbl_userregistration.objects.get(userregistration_email=email)
        otp = random.randint(111111,999999)
        request.session["otp"] = otp
        request.session["fid"] = user.id
        send_mail(
            'Forgot password OTP', #subject
            "\rHello \r" + str(otp) +"\n This is the OTP to reset ur password.\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
            settings.EMAIL_HOST_USER,
            [email],
        )
        return render(request,"Guest/ForgotPassword.html",{"msg":email})
    else:
        return render(request,"Guest/ForgotPassword.html")

def otp(request):
    if request.method == "POST":
        inp_otp = int(request.POST.get("txt_otp"))
        if inp_otp == request.session["otp"]:
            return redirect("Guest:newpass")
        else:
            return render(request,"Guest/OTP.html",{"msg":"OTP Does not Matches..!!"})
    else:
        return render(request,"Guest/OTP.html")

def newpass(request):
    if request.method == "POST":
        user = tbl_userregistration.objects.get(id=request.session["fid"])
        if request.POST.get("txt_new_pass") == request.POST.get("txt_con_pass"):
            user.user_password = request.POST.get("txt_con_pass")
            user.save()
            return render(request,"Guest/NewPassword.html",{"msg1":"Password Updated Sucessfully...."})
        else:
            return render(request,"Guest/NewPassword.html",{"msg":"Error in confirm password..!!!"})
    else:
        return render(request,"Guest/NewPassword.html")   
   