# Generated by Django 4.2.5 on 2023-09-17 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestApp', '0002_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentsMarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registractionNumber', models.CharField(max_length=50)),
                ('marks', models.CharField(max_length=10)),
            ],
        ),
    ]
