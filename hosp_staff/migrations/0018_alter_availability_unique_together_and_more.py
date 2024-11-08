# Generated by Django 5.0.6 on 2024-11-06 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosp_staff', '0017_alter_availability_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='availability',
            unique_together={('doctor', 'available_date')},
        ),
        migrations.AlterField(
            model_name='availability',
            name='day_of_week',
            field=models.CharField(default='Sunday', max_length=9),
        ),
    ]
