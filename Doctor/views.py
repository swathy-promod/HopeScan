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
            return render(request, 'Doctor/Imagepredict.html', {'msg': 'Please select an image.'})

        try:
            img = Image.open(uploaded_file)
        except:
            return render(request, 'Doctor/Imagepredict.html', {'msg': 'Invalid image file.'})

        # Step 1: Validate grayscale / BW
        if not is_grayscale(img):
            return render(request, 'Doctor/Imagepredict.html', {
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

        return render(request,'Doctor/Imagepredict.html',
                      {'prediction': pred_class, 'confidence': confidence})

    return render(request,'Doctor/Imagepredict.html')

# Create your views here.
def myprofiledoctor(request):
    doctordata = tbl_doctorregistration.objects.get(id=request.session['did'])
    return render(request,"Doctor/MyProfileDoctor.html",{'doctordata':doctordata})

def editprofiledoctor(request):
    doctordata=tbl_doctorregistration.objects.get(id=request.session['did'])
    if request.method=="POST":
        name=request.POST.get("txt_name")
        email=request.POST.get("txt_email")
        contact=request.POST.get("txt_contact")
        address=request.POST.get("txt_address")
        doctordata.doctorregistration_name=name
        doctordata.doctorregistration_email=email
        doctordata.doctorregistration_contact=contact
        doctordata.doctorregistration_address=address
        doctordata.save()
        return redirect('Doctor:EditProfileDoctor')
    else:
        return render(request,"Doctor/EditProfileDoctor.html",{'doctordata':doctordata})
    
def changepassworddoctor(request):
    doctordata=tbl_doctorregistration.objects.get(id=request.session['did'])
    if request.method=="POST":
        oldpass=request.POST.get('txt_oldpass')
        newpass=request.POST.get('txt_pass1')
        repass=request.POST.get('txt_pass2')
        if oldpass==doctordata.doctorregistration_password:
            if newpass==repass:
                doctordata.doctorregistration_password=newpass
                doctordata.save()
                return redirect('Doctor:MyProfileDoctor')
            else:
                return render(request,'Doctor/ChangePasswordDoctor.html',{'msg':'mismatch password'})
        else:
            return render(request,'Doctor/ChangePasswordDoctor.html',{'msg':'incorrect password'})    
    return render(request,'Doctor/ChangePasswordDoctor.html')

def homepage(request):
    return render(request,'Doctor/Homepage.html')

def slot(request):
    doctordata= tbl_doctorregistration.objects.get(id=request.session['did'])
    slot_data=tbl_slot.objects.filter(doctor=doctordata)
    if request.method=="POST":
        date=request.POST.get('txt_date') 
        fromtime=request.POST.get('txt_time1')
        totime=request.POST.get('txt_time2')
        count=request.POST.get('txt_count')
        tbl_slot.objects.create(slot_date=date,slot_fromtime=fromtime,slot_totime=totime,slot_count=count,doctor=doctordata)
        return redirect("Doctor:Slot")
    else:
        return render(request, 'Doctor/Slot.html',{'slot':slot_data})

def deleteslot(request,id):
    tbl_slot.objects.get(id=id).delete()
    return redirect("Doctor:Slot")

def viewappointment(request):
    viewdata= tbl_booking.objects.filter(slot__doctor=request.session['did'])
    return render(request,"Doctor/ViewAppointment.html",{'viewdata':viewdata})

def appointmentaccept(request,id):
    slot=tbl_booking.objects.get(id=id)
    slot.booking_status=1
    slot.save()
    return redirect('Doctor:ViewAppointment')

def appointmentreject(request,id):
    slot=tbl_booking.objects.get(id=id)
    slot.booking_status=2
    slot.save()
    return redirect('Doctor:ViewAppointment')

def amount(request,aid):
    appointment = tbl_booking.objects.get(id=aid)
    if request.method == "POST":
        amount = request.POST.get('amount')
        appointment.booking_amount = amount
        appointment.booking_status = 3
        appointment.save()
        return redirect('Doctor:ViewAppointment')
    return render(request, "Doctor/Amount.html", {'appointment': appointment})
