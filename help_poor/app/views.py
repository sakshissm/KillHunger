from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from .forms import SignUpForm,ApplicantForm,AreaForm,DonateForm,ContactForm
from django.core.mail import send_mail
from .models import Driver,Donate
import datetime
# Create your views here.
def index(request):
    return render(request,'app/index.html');

def register(request):
    registered=False
    if request.method=="POST":
        form=SignUpForm(data=request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            registered=True
        else:
            return render(request,'app/error.html',{'error':form.errors})
    else:
        form=SignUpForm()
    return render(request,'app/registration.html',{'form':form,'registered':registered})

def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('app:index'))
            else:
                return HttpResponse("Your account is not active.")
        else:
            return HttpResponse("Invalid credentials.Please try to login again.")
    return render(request,'app/login.html',{});

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:index'))

@login_required
def apply(request):
    if request.method=="POST":
        form=ApplicantForm(data=request.POST)
        if form.is_valid():
            user=form.save()
            if 'profile_pic' in request.FILES:
                user.profile_pic=request.FILES['profile_pic']
            user.save()
            # subject = "Reply"
            message = 'Thank you so much for submitting your application.We will contact you in case we have a required job for you.'
            # send_mail(subject, message, 'shipra112k@gmail.com',[user.email])
            return render(request,'app/thank_candidate.html',{'message':message});
        else:
            return render(request,'app/error.html',{'error':form.errors})
    else:
        form=ApplicantForm()
    return render(request,'app/apply.html',{'form':form})

@login_required
def area(request):
    if request.method=="POST":
        form=AreaForm(data=request.POST)
        if form.is_valid():
            t=form.save()
            t.save()
            # subject = "Reply"
            message = 'Thank you so much for providing information.We appreciate your concern towards poor people.'
            # send_mail(subject, message, 'shipra112k@gmail.com',[t.email])
            return render(request,'app/thank_reporter.html');
        else:
            return render(request,'app/error.html',{'error':form.errors})
    else:
        form=AreaForm()
    return render(request,'app/area.html',{'form':form})


@login_required
def donate(request,pk):
    if request.method=="POST":
        form=DonateForm(data=request.POST)
        if form.is_valid():
            donor = get_object_or_404(User,id=pk)
            user=form.save(commit=False)
            user.donor=donor
            driver_list = list(Driver.objects.filter(allotted_area=user.pincode))
            if not driver_list:
                note='Sorry,our service is not available at your place.'
                return render(request,"app/sorry.html",{'note':note})
            else:
                driver_list = list(Driver.objects.filter(allotted_area=user.pincode,status='Free',employee=True))
                if not driver_list:
                    user.save()
                    note='Currently we don\'t have any free driver to pick up food from your place.We will contact you soon.Sorry for the inconvenience.'
                    return render(request,"app/sorry.html",{'note':note})
                else:
                    driver=driver_list[0]
                    user.driver=driver_list[0].user
                    driver.status='Busy'
                    driver.save()
                    user.flag=1
                    user.save()
                    subject = "Confirmation and details of driver"
                    message = 'Thank you so much for donating food.Here is the details of the driver who is coming to pick food from you:\nName:{} \nMobile Number: {}'.format(driver_list[0].first_name+" "+driver_list[0].last_name,driver_list[0].mobile)
                    send_mail(subject, message, 'sakshiguptamaharani@gmail.com',[user.email])
                    subject2 = "Next Journey"
                    message2 = 'Details:\nOrder Id:{}\nName:{} \nMobile number:{} \nAddress:{} \nLink to location:{} '.format(user.id,user.donor.first_name+" "+user.donor.last_name,user.mobile,user.address,user.location)
                    send_mail(subject2, message2, 'sakshiguptamaharani@gmail.com',[driver_list[0].email])
                    return render(request,'app/thank_donor.html',{'message': message})
        else:
            return render(request,'app/error.html',{'error':form.errors})
    else:
        form=DonateForm()
    return render(request,'app/donate.html',{'form':form})

@login_required
def change_status(request,pk):
    user=get_object_or_404(User,id=pk)
    driver=user.driver
    if request.method=='POST':
        if driver.status=='Free' or driver.status=='Absent':
            return HttpResponse("Your status has already been updated.")
        else:
            driver.status='Free'
            driver.save()
            order_id=request.POST.get('id')
            order=get_object_or_404(Donate,id=order_id)
            order.end_time=datetime.datetime.now()
            order.flag=1
            order.save()
            orders = list(Donate.objects.filter(pincode=driver.allotted_area,flag=0))
            if not orders:
                return render(request,'app/thanks_driver.html',{'message':""})
            else:
                orders[0].flag=1;
                orders[0].save()
                driver.status='Busy'
                driver.save()
                subject = "Confirmation and details"
                message = 'Sorry for being late.Thank you so much for donating food.Here is the details of the driver who is coming to pick food from you:\n Name:{} \n Mobile Number: {}'.format(driver.first_name+" "+driver.last_name,driver.mobile)
                send_mail(subject, message, 'sakshiguptamaharani@gmail.com',[orders[0].email])
                subject2 = "Next Journey"
                message2 = 'Details:\n Id:{} Name:{} \n Mobile:{} \nAddress:{} \nLink to location:{} '.format(orders[0].id,orders[0].donor.first_name+" "+orders[0].donor.last_name,orders[0].mobile,orders[0].address,orders[0].location)
                send_mail(subject2, message2, 'sakshiguptamaharani@gmail.com',[orders[0].email])
                return render(request,'app/thanks_driver.html',{'message': message2})

    else:
        return render(request,'app/status.html',{})


def contact(request,pk):
    if request.method=="POST":
        user=get_object_or_404(User,id=pk)
        form=ContactForm(request.POST)
        enquirer=form.save(commit=False)
        enquirer.user=user
        enquirer.save()
        subject = "Thanks"
        message = "Thank you so much for showing your interest.We will consider your suggestion or resolve your query."
        send_mail(subject, message, 'sakshiguptamaharani@gmail.com',[enquirer.email])
        return render(request,"app/thank_contact.html",{'message':message})
    else:
        form=ContactForm()
        return render(request,'app/contact.html',{'form':form})
