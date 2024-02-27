from django.contrib import admin
from .models import Department,Semester,Teacher,Subject,Student,Mark,Attendance,Announcement,Notice


admin.site.register(Department)
admin.site.register(Semester)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Mark)
admin.site.register(Attendance)
admin.site.register(Announcement)
admin.site.register(Notice)





# Register your models here.
# class TeacherAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Teacher, TeacherAdmin)

# class StudentAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Student,StudentAdmin)

# class StudentsMarksAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(StudentsMarks,StudentsMarksAdmin)