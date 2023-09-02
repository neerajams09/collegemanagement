from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.models import User,auth
from django.contrib import messages
from collegeapp.models import Course,Student,Teacher
import os


# Create your views here.
def index(request):
    return render(request,"login.html")

def course(request):
    return render(request,"add_course.html")

def teacherhome(request):
    return render(request,'teacherhome.html')

def add_course(request):
    if request.method == "POST":
        course_name=request.POST['course_name']
        course_fee=request.POST['fee']
        course=Course(course_name=course_name,fee=course_fee)
        course.save()
        return redirect('course')
    
def student(request):
    courses=Course.objects.all()
    return render(request,"add_student.html",{'course':courses})

def add_student(request):
    if request.method == 'POST':
        student_name=request.POST['name']
        student_address=request.POST['address']
        age=request.POST['age']
        jdate=request.POST['date']
        sel=request.POST['sel']
        course1=Course.objects.get(id=sel)
        student=Student(student_name=student_name,
                        student_address=student_address,
                        student_age=age,
                        joining_date=jdate,
                        course=course1)
        student.save()
        return redirect('show_details')

def home(request):
    return render(request,"home.html")

def log(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        admin=auth.authenticate(username=username, password=password)
        
        if admin is not None:
            if admin.is_staff:
                login(request,admin)
                messages.info(request, f'Welcome {username}')
                return redirect('home')
            else:
                login(request,admin)
                auth.login(request,admin)
                messages.info(request, f'Welcome {username}')
                return redirect('teacherhome')
        else:
            messages.info(request, 'Invalid Username or Password. Please Try Again.')
            return redirect('index')
    else:
        return redirect('index')


def show_details(request):
    student=Student.objects.all()
    return render(request,"show_student.html",{'students':student})

def edit(request,pk):
    student=Student.objects.get(id=pk)
    course=Course.objects.all()
    return render(request,"edit.html",{'stud':student,'course': course})

def edit_student(request,pk):
    if request.method == 'POST':
        student=Student.objects.get(id=pk)
        student.student_name=request.POST['name']
        student.student_address=request.POST['address']
        student.student_age=request.POST['age']
        student.joining_date=request.POST['date']
        sel=request.POST['sel']
        cours=Course.objects.get(id=sel)
        student.course=cours
        student.save()
        return redirect('show_details')

def delete_student(request,pk):
    stu=Student.objects.get(id=pk)
    stu.delete()   
    return redirect('show_details')

def logout(request):
    #if request.user.is_authenticated:
    #request.session["uid"] = ""
    auth.logout(request)
    return redirect('index')


def add_teacher(request):
    if request.method == 'POST':
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        em=request.POST['email']
        age=request.POST['age']
        address=request.POST['address']
        number=request.POST['number']
        image=request.FILES['file']
        sel=request.POST['sel']
        course1=Course.objects.get(id=sel)


        if password==cpassword :
            if User.objects.filter(username=username).exists():
                messages.info(request,"This username already exists!!")
                return redirect('signup')
            else:
                user=User.objects.create_user(first_name=fname,
                                              last_name=lname,
                                              username=username,
                                              password=password,
                                              email=em)
                user.save()
                teacher=Teacher(age=age,address=address,number=number,image=image,course=course1,user=user)
                teacher.save()
                
        else:
            messages.info(request,'Password doesnt match!')
            print("Password not matching")
            return redirect('signup')
        return redirect('signup')
    else:
        return render(request,"signup.html")
def signup(request):
    course=Course.objects.all()
    return render(request,"signup.html",{'course':course})

def profile(request):
    if request.user.is_authenticated:
        current_user=request.user.id
        user1=Teacher.objects.get(user_id=current_user)
        return render(request,'teaprofile.html',{'users':user1})

def teacher_det(request):
    stud=Teacher.objects.all()
    return render(request,'show_teachers.html',{'studen':stud})

def delete_teacher(request,pk):
    det=Teacher.objects.get(user=pk)
    det.delete()
    u=User.objects.get(id=pk)
    u.delete()   
    return redirect('teacher_det')

def edit_teacher(request):
    if request.user.is_authenticated:
        current_user=request.user.id
        print(current_user)
        user1=Teacher.objects.get(user_id=current_user)
        user2=User.objects.get(id=current_user)
        cour=Course.objects.all()
        if request.method == 'POST':
            if len(request.FILES)!=0:
                if len(user1.image)>0:
                    os.remove(user1.image.path)
                user1.image=request.FILES.get('file')
            user2.first_name=request.POST.get('fname')
            user2.last_name=request.POST.get('lname')
            user2.username=request.POST.get('uname')
            user2.email=request.POST.get('mail')
            user1.age=request.POST.get('age')
            user1.number=request.POST.get('mob')
            user1.address=request.POST.get('address')
            sel=request.POST['sel']
            course1=Course.objects.get(id=sel)
            user1.course=course1
            user1.save()
            user2.save()
            return redirect('teacherhome')
        return render(request,'edit_teacher.html',{'users':user1,'course':cour})
    return redirect('/')
   