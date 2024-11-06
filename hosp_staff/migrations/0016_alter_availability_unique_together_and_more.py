# Generated by Django 5.0.6 on 2024-11-06 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosp_staff', '0015_alter_department_dep_image'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='availability',
            unique_together={('doctor', 'available_date')},
        ),
        migrations.AddField(
            model_name='availability',
            name='available_date',
            field=models.DateField(default='2024-01-01'),
        ),
        migrations.RemoveField(
            model_name='availability',
            name='day_of_week',
        ),
    ]