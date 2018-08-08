from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class SignUp(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="donor")
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name

class Applicant(models.Model):
    profile_pic=models.ImageField(upload_to="applicant_pics")
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    dob=models.DateField()
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
    )
    education=models.CharField(max_length=300)
    email=models.EmailField()
    mobile=models.CharField(max_length=10)
    address=models.CharField(max_length=300)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pincode1=models.CharField(max_length=6)
    pincode2=models.CharField(max_length=6)
    pincode3=models.CharField(max_length=6)

    def __str__(self):
        return self.first_name+" "+self.last_name

class AreaReport(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=300)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pincode=models.CharField(max_length=6)
    CATEGORY_CHOICES = (
        ('Old', 'Old'),
        ('Adults', 'Adults'),
        ('Children', 'Children'),
        ('Unknown','Unknown')
    )
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
    )
    people_count=models.PositiveIntegerField(default=0)
    NEED_CHOICES = (
       ('Urgent','Urgent'),
       ('Moderate','Moderate'),
       ('Normal','Normal'),
       ('Unknown','Unknown')
    )
    need=models.CharField(
      max_length=10,
      choices=NEED_CHOICES
    )
    source=models.CharField(max_length=500,default='')
    email=models.EmailField()
    mobile=models.CharField(max_length=10)

    def __str__(self):
        return self.name+","+self.address


class Driver(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="driver")
    profile_pic=models.ImageField(upload_to="staff_pics")
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    dob=models.DateField()
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
    )
    email=models.EmailField()
    mobile=models.CharField(max_length=10)
    address=models.CharField(max_length=300)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    allotted_area=models.CharField(max_length=6)
    joining_date=models.DateTimeField()
    leaving_date=models.DateTimeField(null=True,blank=True)
    employee=models.BooleanField(default=True)
    STATUS_CHOICES=(
        ('Free', 'Free'),
        ('Busy', 'Busy'),
        ('Absent', 'Absent')
    )
    status=models.CharField(
      max_length=10,
      choices=STATUS_CHOICES,
    )
    salary=models.PositiveIntegerField()
    def __str__(self):
        return self.first_name+" "+self.last_name

class Donate(models.Model):
    donor=models.ForeignKey(User,on_delete=models.CASCADE,related_name='access_donor')
    food_description=models.TextField()
    purpose=models.CharField(max_length=300)
    address=models.CharField(max_length=300)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pincode=models.CharField(max_length=6)
    location=models.URLField()
    email=models.EmailField()
    mobile=models.CharField(max_length=10)
    start_time=models.DateTimeField(auto_now_add=True)
    driver=models.ForeignKey(User,on_delete=models.CASCADE,related_name='access_driver',null=True)
    end_time=models.DateTimeField(null=True)
    flag=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.donor.username

class Contact(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='enquirer')
    name=models.CharField(max_length=50)
    email=models.EmailField()
    subject=models.CharField(max_length=100)
    message=models.TextField()

    def __str__(self):
        return self.subject
