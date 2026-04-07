from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('course/create/', views.create_course, name='create_course'),
    path('course/<int:course_id>/', views.teacher_course_detail, name='teacher_course_detail'),
    path('course/<int:course_id>/assignment/create/', views.create_assignment, name='create_assignment'),
    path('assignment/<int:assignment_id>/grades/', views.grade_submissions, name='grade_submissions'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('student/course/<int:course_id>/', views.student_course_detail, name='student_course_detail'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
]
