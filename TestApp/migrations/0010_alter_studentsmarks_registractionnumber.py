# Generated by Django 4.2.5 on 2023-09-21 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestApp', '0009_remove_studentsmarks_marks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsmarks',
            name='registractionNumber',
            field=models.CharField(max_length=50),
        ),
    ]
