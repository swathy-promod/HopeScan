from operator import le

from django.shortcuts import render,redirect
from Guest.models import *
from User.models import *
from Doctor.models import *


from django.db import transaction
import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf
from keras.models import Model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import os
from PIL import Image
# Create your views here.


MODEL_PATH = os.path.join("Assets", "Model", "vgg16_breast_cancer_ultrasound.keras")
model = load_model(MODEL_PATH)

def predict_image(pil_img):
    pil_img = pil_img.resize((128, 128))
    img_array = image.img_to_array(pil_img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_array, verbose=0)
    print("Raw prediction:", preds)
    print("Shape:", preds.shape)

    prob = preds[0][0]
    pred_class = "Malignant" if prob > 0.6 else "Benign"
    return pred_class, prob

from PIL import Image
import numpy as np

# -------------------------
# Grayscale/BW Check
# -------------------------
def is_grayscale(img):
    """
    Returns True if the image is grayscale / black & white.
    """
    # Convert non-standard modes to RGB
    if img.mode not in ("L", "RGB"):
        img = img.convert("RGB")

    img_array = np.array(img)

    # Single-channel → grayscale
    if len(img_array.shape) == 2:
        return True

    # 3-channel RGB → check if R=G=B for all pixels
    if len(img_array.shape) == 3 and img_array.shape[2] == 3:
        if np.all(img_array[:,:,0] == img_array[:,:,1]) and np.all(img_array[:,:,1] == img_array[:,:,2]):
            return True

    return False


def Imagepredict(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file_photo')

        if not uploaded_file:
            return render(request, 'User/Imagepredict.html', {'msg': 'Please select an image.'})

        try:
            img = Image.open(uploaded_file)
        except:
            return render(request, 'User/Imagepredict.html', {'msg': 'Invalid image file.'})

        # Step 1: Validate grayscale / BW
        if not is_grayscale(img):
            return render(request, 'User/Imagepredict.html', {
                'msg': 'Invalid Image: Please upload a real breast scan (Ultrasound / Mammogram) in grayscale/BW.'
            })

        # Step 2: Predict cancer
        pred_class, prob = predict_image(img)
        confidence = round(prob * 100, 2)

        # # # Step 3: Save in DB
        # # user_id = request.session.get("uid")
        # # tbl_aiconsultation.objects.create(
        # #     user_id=user_id,
        # #     consultation_type="Image",
        # #     uploaded_image=uploaded_file,
        # #     ai_result=pred_class,
        # #     ai_confidence=confidence
        # )

        return render(request,'User/Imagepredict.html',
                      {'prediction': pred_class, 'confidence': confidence})

    return render(request,'User/Imagepredict.html')

def Homepage(request):
    userdata = tbl_userregistration.objects.get(id=request.session['uid'])
    # provide upcoming appointments and quick counts for the homepage
    upcoming = tbl_booking.objects.filter(user=request.session['uid']).order_by('booking_date')[:5]
    counts = {
        'appointments': tbl_booking.objects.filter(user=request.session['uid']).count(),
        'doctors': tbl_doctorregistration.objects.count(),
    }
    return render(request,"User/Homepage.html",{'userdata':userdata,'upcoming':upcoming,'counts':counts})

def Myprofile(request):
    userdata = tbl_userregistration.objects.get(id=request.session['uid'])
    # add simple stats for the profile page
    appointment_count = tbl_booking.objects.filter(user=request.session['uid']).count()
    return render(request,"User/MyProfile.html",{'userdata':userdata,'appointment_count':appointment_count})

def editprofile(request):
    userdata=tbl_userregistration.objects.get(id=request.session['uid'])
    if request.method=="POST":
        name=request.POST.get("txt_name")
        email=request.POST.get("txt_email")
        contact=request.POST.get("txt_contact")
        address=request.POST.get("txt_address")
        userdata.userregistration_name=name
        userdata.userregistration_email=email
        userdata.userregistration_contact=contact
        userdata.userregistration_address=address
        userdata.save()
        return redirect('User:EditProfile')
    else:
        return render(request,"User/EditProfile.html",{'userdata':userdata})
    
def changepassword(request):
    userdata=tbl_userregistration.objects.get(id=request.session['uid'])
    if request.method=="POST":
        oldpass=request.POST.get('txt_oldpass')
        newpass=request.POST.get('txt_pass1')
        repass=request.POST.get('txt_pass2')
        if oldpass==userdata.userregistration_password:
            if newpass==repass:
                userdata.userregistration_password=newpass
                userdata.save()
                return redirect('User:Myprofile')
            else:
                return render(request,'User/ChangePassword.html',{'msg':'mismatch password'})
        else:
            return render(request,'User/ChangePassword.html',{'msg':'incorrect password'})    
    return render(request,'User/ChangePassword.html')

def complaint(request):
    complaintdata=tbl_complaint.objects.filter(user=request.session['uid'])
    userdata=tbl_userregistration.objects.get(id=request.session['uid'])
    if request.method=='POST':
        title=request.POST.get('txt_title')
        content=request.POST.get('txt_content')
        tbl_complaint.objects.create(complaint_title=title,
                                     complaint_content=content,
                                     user=userdata)
        return render(request,'User/Complaint.html',{'msg':'complaint Added'})
    else:
        return render(request,'User/Complaint.html',{'comp':complaintdata})
    
def feedback(request):
    feedback=tbl_feedback.objects.filter(user=request.session['uid'])
    if request.method=='POST':
        content=request.POST.get("txt_feed")
        tbl_feedback.objects.create(feedback_content=content,
                                    user=tbl_userregistration.objects.get(id=request.session['uid']))
        return redirect("User:Feedback")
    else:
        return render(request,"User/Feedback.html",{'feedback':feedback})
    
def viewsdoctor(request):
    viewsdoctor=tbl_doctorregistration.objects.all()
    return render(request,"User/ViewsDoctor.html",{'doctorregistration_data':viewsdoctor})
        
def bookappointment(request,id):
    book=tbl_slot.objects.filter(doctor=id)
    if request.method=="POST":
        slot_id=request.POST.get('select_slot')
        slot=tbl_slot.objects.get(id=slot_id)
        tbl_booking.objects.create(
            booking_time=slot.slot_fromtime,
            slot=slot,
            user=tbl_userregistration.objects.get(id=request.session['uid'])
        )
        return redirect("User:MyAppointment")
    else:
        return render(request,"User/Bookappointment.html",{'slot':book})
    
def myappointment(request):
    viewappointment=tbl_booking.objects.filter(user=request.session['uid'])
    return render(request,"User/MyAppointment.html",{'booking_data':viewappointment})

def payment(request,id):
    paydata=tbl_booking.objects.get(id=id)
    if request.method=='POST':
        paydata.booking_status=4
        paydata.save()
        return redirect('User:MyAppointment')
    else:
        return render(request,'User/Payment.html',{'paydata':paydata})



 

    