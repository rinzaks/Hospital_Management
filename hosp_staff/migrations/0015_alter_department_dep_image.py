# Generated by Django 5.0.6 on 2024-11-05 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosp_staff', '0014_employee_deleted_at_employee_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='dep_image',
            field=models.ImageField(blank=True, null=True, upload_to='departments'),
        ),
    ]