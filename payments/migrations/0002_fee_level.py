# Generated by Django 5.1.1 on 2024-10-13 08:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
        ('students', '0011_alter_faculty_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='fee',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.level'),
        ),
    ]
