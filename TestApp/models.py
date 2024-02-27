from django.db import models
from django.contrib.auth.models import User
# Create your models here.


dept = [('MCA', 'Master of Computer Applications'), ('BCA', 'Bachelor of Computer Applications')]
sem = [('1st', '1st Semester'), ('2nd', '2nd Semester'), ('3rd', '3rd Semester'), ('4th', '4th Semester'),
       ('5th', '5th Semester'), ('6th', '6th Semester'), ('7th', '7th Semester'), ('8th', '8th Semester')]
sub = [('Python', 'Python'),('COA','COA'),('Discrete Mathematics','Discrete Mathematics'),('DBMS', 'Database Management System'),('Data Structure','Data Structure') ,('Java', 'Java'),
       ('Operating System','Operation System'),('Networking','Networking'),('Computer Graphics','computer Graphics'),('DAA','Design and Analysis of algorithms'),
       ('Software engineering','Software engineering'), ('ML', 'Machine Learning'), ('AI', 'Artificial Intelligence'),('DS','Basic Data Science')]

class Department(models.Model):
    name=models.CharField(max_length=10,choices=dept,default="Select Department")

    def __str__(self):
        return self.name

class Semester(models.Model):
    semester=models.CharField(max_length=10,choices=sem,default='Select Semester')
    department=models.ForeignKey(Department,on_delete=models.CASCADE)

    def __str__(self):
        return self.semester 

class Subject(models.Model):
    name=models.CharField(max_length=50,choices=sub,default='Select Subject')
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE)

    def __str__(self):
        return self.name 

class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50,null=False,default=None)
    last_name=models.CharField(max_length=50,null=False,default=None)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester_taught=models.ManyToManyField(Semester)
    subject_taught=models.ManyToManyField(Subject)

    def __str__(self):
        return '{} {}'.format(self.first_name,self.last_name)
    



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50,null=False)
    last_name=models.CharField(max_length=50,null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semesters_enrolled = models.ManyToManyField(Semester)
    subjects = models.ManyToManyField(Subject)
    registration_number = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    

    def __str__(self):
        return '{} {}'.format(self.first_name,self.last_name)
    
class Mark(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    date_recode=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.subject} - Marks: {self.marks_obtained}"


class Attendance(models.Model):
    date = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=10,choices=(('Present','Present'),('Absent','Absent')))

    def __str__(self):
        return "{}-{}-{}".format(self.date,self.department,self.student)


class Announcement(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    date_created=models.DateField(auto_now_add=True)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE,default=None)

    def __str__(self):
        return "{} --{}".format(self.title,self.teacher)
    

class Notice(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    pdf_file=models.FileField(upload_to='notices/')
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

