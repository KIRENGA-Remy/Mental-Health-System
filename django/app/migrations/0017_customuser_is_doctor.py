# Generated by Django 5.1.2 on 2024-11-25 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_patientmodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_doctor',
            field=models.BooleanField(default=False),
        ),
    ]