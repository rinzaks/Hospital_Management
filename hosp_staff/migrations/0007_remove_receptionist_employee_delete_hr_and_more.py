# Generated by Django 5.1.2 on 2024-10-22 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hosp_staff', '0006_remove_nurse_shift'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receptionist',
            name='employee',
        ),
        migrations.DeleteModel(
            name='HR',
        ),
        migrations.DeleteModel(
            name='Receptionist',
        ),
    ]