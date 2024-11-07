from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('stddashboard/', views.student_dashboard, name='student_dashboard'),
    path('instructor_dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('courses/', views.course_list, name='courses'),
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/enroll/<int:course_id>/', views.enroll, name='enroll'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
]
