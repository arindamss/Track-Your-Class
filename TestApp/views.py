from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import Group
from django.urls import reverse
from . import forms, models
from django.core.files.storage import FileSystemStorage
# from django.shortcuts import get_object_or_404
# from django.conf import settings
# import os




def home(request):
    # notices = models.Notice.objects.all()
    return render(request, 'index.html')


# def download_pdf(request, pdf_id):
#     notice = get_object_or_404(models.Notice, id=pdf_id)
#     file_path = os.path.join(settings.MEDIA_ROOT, str(notice.pdf_file))
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as pdf:
#             response = HttpResponse(pdf.read(), content_type='application/pdf')
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
#     else:
#         return HttpResponse("File not found", status=404)

def noticebord(request):
    notices = models.Notice.objects.all()
    return render(request,'notice.html',{'notice':notices})



def student_signup_view(request):
    if request.method == "POST":
        userForm=forms.StudentUserForm(request.POST)
        if userForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            reg_num=request.POST.get('reg_num')
            dept_id=request.POST.get('dept')
            sem_enrol=request.POST.getlist('semester')
            subjects_chose=request.POST.getlist('sub')

            student=models.Student(
                first_name=first_name,
                last_name=last_name,
                registration_number=reg_num,
                department=models.Department.objects.get(id=dept_id),
                user=user
            )
            student.save()

            student.semesters_enrolled.set(sem_enrol)

            student.subjects.set(subjects_chose)

            my_students_group, created = Group.objects.get_or_create(name='STUDENT')
            my_students_group.user_set.add(user)

            return HttpResponse("Student is Added, Now you Can Login")
        else:
            return HttpResponse("UserForm is not Valid")
    
    mydict={
        'userForm':forms.StudentUserForm(),
        'dept':models.Department.objects.all(),
        'semester':models.Semester.objects.all(),
        'subject':models.Subject.objects.all(),
    }
    return render(request,'student_signup.html',context=mydict)


def is_admin(user):
    if (user is not None) and (user.is_staff):
        return True
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('adminview')
    elif is_teacher(request.user):
        return redirect('teacher_dashbord')
    elif is_student(request.user):
        cridencial=models.Student.objects.all().filter(user_id=request.user.id,status=True)
        if cridencial:
            return redirect('student_dashbord')
        elif models.Student.objects.all().filter(user_id=request.user.id,status=False):
            return redirect('student_rejected')
        else:
            return redirect('student_waiting')






@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def adminview(request):
        return render(request,'adminview.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def add_teacher_view(request):
    if request.method == "POST":
        userForm = forms.TeacherUserForm(request.POST)
        if userForm.is_valid():
            # Save the user information
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            # Get other form fields
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            dept_id = request.POST.get('dept')
            semesters = request.POST.getlist('semester')  # Assuming semester is a checkbox input
            sub=request.POST.getlist('sub_tat')

            # Create a Teacher instance and associate it with the user
            teacher = models.Teacher(
                first_name=first_name,
                last_name=last_name,
                department=models.Department.objects.get(id=dept_id),
                user=user
            )
            teacher.save()
            

            # Add selected semesters to the teacher's semester_taught many-to-many field
            teacher.semester_taught.add(*semesters)

            teacher.subject_taught.set(sub)

            # Add the teacher to the 'TEACHER' group
            my_teacher_group, created = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group.user_set.add(user)

            return HttpResponse("Teacher Added Successfully")
        else:
            return HttpResponse("Form Validation Failed")
    
    # If it's a GET request, render the form
    mydict = {'userForm': forms.TeacherUserForm(),
              'dept': models.Department.objects.all(),
              'semester': models.Semester.objects.all(),
              'sub':models.Subject.objects.all()}
    return render(request, 'add_teacher.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_student(request):
    student=models.Student.objects.all().filter(status=False)
    return render(request,'admin_approve_students.html',{'student':student})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_student(request,sid):
    student=models.Student.objects.get(id=sid)
    student.status=True
    student.save()
    return redirect(reverse('admin_approve_student'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_student(request,sid):
    student=models.Student.objects.get(id=sid)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin_approve_student')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def checkAttendance(request):
    department=models.Department.objects.all()
    semester=models.Semester.objects.all()
    if request.method =="POST":
        dept_id=request.POST.get("dept_id")
        sem_id=request.POST.get("sem_id")

        dept=models.Department.objects.get(id=dept_id)
        sem=models.Semester.objects.get(id=sem_id)
        students=models.Student.objects.filter(department=dept,semesters_enrolled=sem,status=True)
        total_class=models.Attendance.objects.filter(department=dept,semester=sem).count()
        students_count=models.Student.objects.filter(department=dept,semesters_enrolled=sem,status=True).count()
        attendance_list=models.Attendance.objects.filter(department=dept,semester=sem)
        percentage={}
        if students_count>0:
            total_class=int(total_class/students_count)
            for s in students:
                total_present=models.Attendance.objects.filter(department=dept,semester=sem,student=s,status='Present').count()
                overall_percentage=(total_present / total_class)*100
                overall_percentage=int(overall_percentage)
                percentage[s]=overall_percentage
            return render(request,'checkAttendance.html',{'attendance':attendance_list,'percentage':percentage,'department':department,'semester':semester})
        else:
            return render(request,'checkAttendance.html',{'department':department,'semester':semester,'empty':0})
    
    return render(request,'checkAttendance.html',{'department':department,'semester':semester})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def TeacherList(request):
    departments=models.Department.objects.all()
    teachers=models.Teacher.objects.all()
    if request.method == 'POST':
        dep_id=request.POST.get('dept_id')
        department_ins=models.Department.objects.get(id=dep_id)
        teacher=models.Teacher.objects.filter(department=department_ins)
        mydict={'department':departments,
            'teacher':teacher}
        return render(request,'TeacherList.html',context=mydict)
    
    mydict={'department':departments,
            'teacher':teachers}
    return render(request,'TeacherList.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher(request,t_id):
    teacher=models.Teacher.objects.get(id=t_id)
    teacher.delete()
    return redirect('TeacherList')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def uploadNotice(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        pdf_file = request.FILES['pdf_file']
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        uploaded_file_url = fs.url(filename)
        models.Notice.objects.create(title=title, description=description, pdf_file=uploaded_file_url)
        return redirect('adminview')  # Assuming the home URL name is 'home'
    return render(request, 'uploadNotice.html')




# -------------------------------Teacher View ---------------------------------
# -----------------------------------------------------------------------------
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashbord_view(request):
    teacher=models.Teacher.objects.get(user_id=request.user.id)
    return render(request,'teacher_dashbord.html',{'teacher':teacher})




@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def semester_list(request,t_id):
    teacher=models.Teacher.objects.get(id=t_id)
    teacher_semester=teacher.semester_taught.all()
    return render(request,'select_department.html',{'semester':teacher_semester,'teacher':teacher})



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def assign_marks(request,sem,t_id):
    if request.method == "POST":
        teacher=models.Teacher.objects.get(id=t_id)
        teacher_department=teacher.department
        subject_id=request.POST.get('sub_id')
        sub_id=models.Subject.objects.get(id=subject_id)
        semester=models.Semester.objects.get(id=sem)
        # marks_obtained=request.POST.get('marks_obtain')
        students=models.Student.objects.filter(department=teacher_department,semesters_enrolled=sem,status=True)
        for student in students: 
            # mark=request.POST.get(f'marks_{student.id}')
            marks=request.POST.get(f'marks_{student.id}')
            if marks is not None and marks.isdigit():
                marks=models.Mark(
                    teacher=models.Teacher.objects.get(id=t_id),
                    student=models.Student.objects.get(id=student.id),
                    subject=sub_id,
                    semester=semester,
                    marks_obtained=marks
                )
                marks.save()
                # print(mark)
                
            else:
                return HttpResponse("Invalid Marks")
        return HttpResponse("Marks Submited")

    
    teacher=models.Teacher.objects.get(id=t_id)
    subject=list(teacher.subject_taught.all())
    teacher_department=teacher.department
    students=models.Student.objects.filter(department=teacher_department,semesters_enrolled=sem,status=True)

    mydict={
        'students':students,
        'subject':subject,
        'dept':teacher.department,
        'sem':models.Semester.objects.filter(id=sem).first()
    }
    return render(request,'assign_marks.html',context=mydict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def make_attendance(request,t_id):
    if request.method == "POST":
        sem_id=request.POST.get('sem_id')
        sub_id=request.POST.get('sub_id')
        teacher=models.Teacher.objects.get(id=t_id)
        t_id=teacher.id
        d_id=teacher.department.id
        print(d_id)
        print(t_id)
        print(sem_id)
        print(sub_id)

        url=reverse('fill_attendance', args=[t_id,d_id,sem_id,sub_id])
        return redirect(url)

    teacher=models.Teacher.objects.get(id=t_id)
    semester_list=teacher.semester_taught.all()
    subject_list=teacher.subject_taught.all()
    return render(request,'attendance_semester_list.html',{'semester_list':semester_list,'subject':subject_list,'teacher':teacher})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def fill_attendance(request,t_id,d_id,sem_id,sub_id):
    teacher_ins=models.Teacher.objects.get(id=t_id)
    subject_ins=models.Subject.objects.get(id=sub_id)
    department_ins=models.Department.objects.get(id=d_id)
    semester_ins=models.Semester.objects.get(id=sem_id)
    students=models.Student.objects.all().filter(department=department_ins,semesters_enrolled=semester_ins,status=True)
    if request.method == "POST":
        for s in students:
            student_ins=models.Student.objects.get(id=s.id)
            status = request.POST.get(f'status_{s.id}','Absent')
            if status in ('Present','Absent'):
                attendance=models.Attendance(teacher=teacher_ins,department=department_ins,semester=semester_ins,subject=subject_ins,student=student_ins,status=status)
                attendance.save()
        return HttpResponse("Attendance Taken")

    return render(request,'take_attendance.html',{'students':students})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def checkAttendance_Teacher(request,t_id):
    teacher=models.Teacher.objects.get(id=t_id)
    sems=teacher.semester_taught.all()
    if request.method=="POST":
        sem=request.POST.get('sem_id')
        dept=teacher.department
        subject=teacher.subject_taught.all()
        print(dept)
        print(sem)
        print(subject)

        total_class=models.Attendance.objects.filter(department=dept,semester=sem,subject__in=subject).count()
        students_count=models.Student.objects.filter(department=dept,semesters_enrolled=sem,status=True).count()
        
        students=models.Student.objects.filter(department=dept,semesters_enrolled=sem,status=True)
        attendance_list=models.Attendance.objects.filter(department=dept,semester=sem,subject__in=subject)
        percentage={}
        if students_count>0: # if that semester contain any student then if block execute outherwise else
            total_class=int(total_class/students_count)
            for s in students:
                total_present=models.Attendance.objects.filter(department=dept,semester=sem,student=s,subject__in=subject,status='Present').count()
                overall_percentage=(total_present / total_class)*100
                overall_percentage=int(overall_percentage)
                percentage[s]=overall_percentage
                print(total_class)
            return render(request,'checkAttendance_Teacher.html',{'attendance':attendance_list,'percentage':percentage,'semester':sems,'total_class':total_class})
        else:
            return render(request,'checkAttendance_Teacher.html',{'semester':sems,'empty':1})

    return render(request,'checkAttendance_Teacher.html',{'semester':sems})


def studentList(request):
    teacher=models.Teacher.objects.get(user_id=request.user.id)
    department=teacher.department
    semesters=teacher.semester_taught.all()
    if request.method == 'POST':
        sem=request.POST.get('sem_id')
        semester=models.Semester.objects.get(id=sem)
        students=models.Student.objects.filter(department=department,semesters_enrolled=semester)
        return render(request,'studentList.html',{'semesters':semesters,'students':students,'semester':semester})
    return render(request,'studentList.html',{'semesters':semesters})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def announcement(request):
    teacher=models.Teacher.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        sem_id=request.POST.get('sem_id')
        semester=models.Semester.objects.get(id=sem_id)
        announcement=models.Announcement(title=title,description=description)
        announcement.teacher=teacher
        announcement.department=teacher.department
        announcement.semester=semester

        announcement.save()
        return redirect("teacher_dashbord")
    semester=teacher.semester_taught.all()
    return render(request,'announcement.html',{'semester':semester})







# ---------------------------------Student View---------------------------------
# ------------------------------------------------------------------------------
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashbord_view(request):
    student=models.Student.objects.get(user_id=request.user.id)
    department=student.department
    semester=student.semesters_enrolled.all()
    for i in semester:
        sem=i
    announcement=models.Announcement.objects.filter(department=department,semester=semester[0])
    return render(request,'student_dashbord.html',{'student':student,'announcement':announcement,'sem':sem})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_waiting_view(request):
    return render(request,'student_waiting.html')

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_marks(request):
    student = models.Student.objects.get(user=request.user)
    marks = models.Mark.objects.filter(student=student)
    return render(request, 'view_marks.html', {'student': student, 'marks': marks})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def track_attendance(request):
    student=models.Student.objects.get(user_id=request.user.id)
    subjects=student.subjects.all()
    percentage={}
    print("------",subjects)
    for subject in subjects:
        total_class=models.Attendance.objects.filter(student=student,subject=subject).count()
        total_present=models.Attendance.objects.filter(student=student,subject=subject,status='Present').count()

        if total_class>0:
            overall_percentage=int((total_present/total_class)*100)
            percentage[subject.name]=overall_percentage
        else:
            percentage[subject.name]=0
    return render(request,'track_attendance.html',{'percentage':percentage})



def announcementById(request,a_id):
    announcement=models.Announcement.objects.get(id=a_id)
    return render(request,'announcement_view.html',{'announcement':announcement})