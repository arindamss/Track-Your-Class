# Generated by Django 4.2.5 on 2023-09-22 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestApp', '0012_department_semester_remove_student_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='registration_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
