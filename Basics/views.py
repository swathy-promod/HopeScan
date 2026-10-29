
from django.shortcuts import render,redirect

def calculator(request):
    if request.method == "POST":
        num1 = int(request.POST.get("txt_num1"))
        num2 = int(request.POST.get("txt_num2"))
        btn = request.POST.get("btn_submit")
        if btn == '+':
            result = num1 + num2
        elif btn == '-':
            result = num1 - num2
        else:
            result = num1 * num2
        return render(request,"Calculator.html",{'result':result})
    else:
        return render(request,"Calculator.html")

def largest(request):
    if request.method == 'POST':
        num1 = int(request.POST.get("txt_num1"))
        num2 = int(request.POST.get("txt_num2"))
        if num1 > num2:
            result = num1
        else:
            result = num2
        return render(request, 'Largest.html', {'result': result})
    else:   
        return render(request, 'Largest.html')

def largestof3(request):
    if request.method == 'POST':
        num1 = int(request.POST.get("txt_num1"))
        num2 = int(request.POST.get("txt_num2"))
        num3 = int(request.POST.get("txt_num3"))
        if num1 >= num2 and num1 >= num3:
            result = num1
        elif num2 >= num1 and num2 >= num3:
            result = num2
        else:
            result = num3
        return render(request, 'Largestof3.html', {'result': result})
    else:
        return render(request, 'Largestof3.html')

def Sum(request):
    if request.method == 'POST':
        num1 = int(request.POST.get("txt_num1"))
        num2 = int(request.POST.get("txt_num2"))
        result = num1 + num2
        return render(request, 'Sum.html', {'result': result})
    else:
        return render(request, 'Sum.html')
        

    

