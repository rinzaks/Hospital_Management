# Generated by Django 5.1.2 on 2024-10-21 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hosp_staff', '0004_department_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='specialization',
        ),
    ]