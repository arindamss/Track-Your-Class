# Generated by Django 4.2.5 on 2023-09-26 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestApp', '0016_alter_studentsmarks_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='subject_taught',
            field=models.ManyToManyField(to='TestApp.subject'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(choices=[('Python', 'Python'), ('Java', 'Java'), ('COA', 'Computer Organization and Architecture'), ('DBMS', 'Database Management System'), ('ML', 'Machine Learning'), ('AI', 'Artificial Intelligence')], default='Select Subject', max_length=50),
        ),
    ]
