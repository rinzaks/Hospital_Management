# Generated by Django 5.1.2 on 2024-11-01 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hosp_user', '0002_delete_invoice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicalhistory',
            old_name='past_conditions',
            new_name='illness',
        ),
    ]