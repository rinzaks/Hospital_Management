# Generated by Django 5.0.6 on 2024-11-06 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosp_staff', '0016_alter_availability_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='availability',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='availability',
            name='day_of_week',
            field=models.CharField(default='sunday', max_length=9),
        ),
        migrations.AlterUniqueTogether(
            name='availability',
            unique_together={('doctor', 'day_of_week')},
        ),
    ]
