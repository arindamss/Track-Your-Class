# Generated by Django 4.2.5 on 2023-09-18 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestApp', '0004_alter_studentsmarks_registractionnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='subject',
            field=models.CharField(choices=[('Python (MCA)', 'Python (MCA)'), ('Java (MCA)', 'Java (MCA)'), ('DAA (MCA)', 'DAA (MCA)'), ('COA (MCA)', 'COA (MCA)'), ('C Programmin (BCA)', 'C Programmin (BCA)'), ('Digital Electronics (BCA)', 'Digital Electronics (BCA)'), ('Aritifical Inteligence (BCA)', 'Aritifical Inteligence (BCA)'), ('Aritifical Inteligence (CSE)', 'Aritifical Inteligence (CSE)'), ('Machine Learning (CSE)', 'Machine Learning (CSE)'), ('Electric Circuit Theory (EE)', 'Electric Circuit Theory (EE)'), ('Digital Electronic  (EE)', 'Digital Electronic (EE)'), ('Power electronics (EE)', 'Power electronics (EE)'), ('Electronic Devices (ECE)', 'Electronic Devices (ECE)'), ('Analog Communication  (ECE)', 'Analog Communication (ECE)'), ('Microprocessor &Microcontrollers (ECE)', 'Microprocessor &Microcontrollers (ECE)')], default='Subject', max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='department',
            field=models.CharField(choices=[('MCA', 'MCA'), ('BCA', 'BCA'), ('CSE', 'CSE'), ('EE', 'EE'), ('ECE', 'ECE')], default='MCA', max_length=50),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='department',
            field=models.CharField(choices=[('MCA', 'MCA'), ('BCA', 'BCA'), ('CSE', 'CSE'), ('EE', 'EE'), ('ECE', 'ECE')], default='MCA', max_length=50),
        ),
    ]
