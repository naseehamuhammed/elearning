from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, CourseForm
from .models import Course, UserProfile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            UserProfile.objects.create(user=user, role=role)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_dashboard') 
                elif hasattr(user, 'userprofile') and user.userprofile.role == 'instructor':
                    return redirect('instructor_dashboard')  
                else:
                    return redirect('student_dashboard')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.role == 'Instructor':
        return redirect('instructor_dashboard')
    else:
        return render(request, 'dashboard.html')


@login_required
def instructor_dashboard(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'instructor_dashboard.html', {'courses': courses})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if course.instructor != request.user:
        return redirect('instructor_dashboard')  

    if request.method == 'POST':
        course.delete()
        return redirect('instructor_dashboard')
    
    return render(request, 'confirm_delete.html', {'course': course})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.instructor != request.user:
        return redirect('instructor_dashboard') 
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('instructor_dashboard')
    else:
        form = CourseForm(instance=course)

    return render(request, 'edit_course.html', {'form': form})


@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('instructor_dashboard')
    else:
        form = CourseForm()
    return render(request, 'create_course.html', {'form': form})

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})


@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.students.add(request.user)  
    return redirect('courses')


@login_required
def student_dashboard(request):
    
    courses = Course.objects.all()
    enrolled_courses = Course.objects.filter(students=request.user)
    last_accessed_course_id = request.session.get('last_accessed_course')
   
    if last_accessed_course_id:
        last_accessed_course = Course.objects.get(id=last_accessed_course_id)
    else:
        last_accessed_course = None 

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        if 'enroll_course' in request.POST:
            if request.user not in course.students.all():
                course.students.add(request.user)
                course.save()
            return redirect('student_dashboard') 

    return render(request, 'student_dashboard.html', {
        'courses': courses,
        'enrolled_courses': enrolled_courses,
        'last_accessed_course': last_accessed_course

    })

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    request.session['last_accessed_course'] = course.id
    return render(request, 'course_detail.html', {'course': course})


@login_required
def admin_dashboard(request):
    user=User.objects.all()
    courses= Course.objects.all()
    return render(request, 'admin_dashboard.html',{'user' : user ,'courses':courses})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('admin_dashboard') 
    return render(request, 'confirm_delete.html', {'course': course}) 
