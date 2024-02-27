"""
URL configuration for TestProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from TestApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('adminlogin',LoginView.as_view(template_name='adminlogin.html'),name='adminlogin'),
    path('teacherlogin',LoginView.as_view(template_name='teacherlogin.html'),name='teacherlogin'),
    path('studentlogin',LoginView.as_view(template_name='student_login.html'),name='studentlogin'),

    path('afterlogin',views.afterlogin_view,name='afterlogin'),

    path('logout',LogoutView.as_view(template_name='index.html'),name='logout'),

    path('notice',views.noticebord,name='notice'),

    # path('download_pdf/<int:pdf_id>/', views.download_pdf, name='download_pdf'),

    
    
    # admin URLS
    path('adminview',views.adminview,name='adminview'),
    path('add_teacher/',views.add_teacher_view,name='add_teacher'),
    path('admin_approve_student',views.admin_approve_student,name='admin_approve_student'),
    path('approve_student/<int:sid>',views.approve_student,name='approve_student'),
    path('reject_student/<int:sid>',views.reject_student,name='reject_student'),
    path("checkAttendance",views.checkAttendance,name="checkAttendance"),
    path('TeacherList',views.TeacherList,name='TeacherList'),
    path('delete_teacher,<t_id>',views.delete_teacher,name='delete_teacher'),
    path('uploadNotice', views.uploadNotice, name='uploadNotice'),
    # path('uploadNotice/', views.uploadNotice, name='uploadNotice'),

    # Teacher URLS
    path('teacher_dashbord',views.teacher_dashbord_view,name='teacher_dashbord'),
    path('fill_marks/<t_id>',views.semester_list,name='fill_marks'),
    path('assign_marks/<sem>/<t_id>',views.assign_marks,name='assign_marks'),
    path('make_attendance/<t_id>',views.make_attendance,name='make_attendance'),
    path('fill_attendance/<t_id>/<d_id>/<sem_id>/<sub_id>',views.fill_attendance,name='fill_attendance'),
    path('checkAttendance_Teacher/<t_id>',views.checkAttendance_Teacher,name='checkAttendance_Teacher'),
    path('studentList',views.studentList,name='studentList'),
    path('announcement',views.announcement,name='announcement'),
    
    # Students URLS
    path('studentsignup',views.student_signup_view,name='studentsignup'),
    path('student_dashbord',views.student_dashbord_view,name='student_dashbord'),
    path('student_waiting',views.student_waiting_view,name='student_waiting'),
    path('view_marks',views.view_marks,name='view_marks'),
    path('track_attendance',views.track_attendance,name='track_attendance'),
    path('announcement/<a_id>',views.announcementById,name='announcement'),


    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
