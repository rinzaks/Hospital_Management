# Generated by Django 5.1.2 on 2024-11-02 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosp_user', '0003_rename_past_conditions_medicalhistory_illness'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='name',
            field=models.CharField(default='name', max_length=255),
        ),
    ]
