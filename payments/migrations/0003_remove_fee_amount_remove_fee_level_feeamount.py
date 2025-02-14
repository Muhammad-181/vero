# Generated by Django 5.1.1 on 2024-10-13 08:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_fee_level'),
        ('students', '0011_alter_faculty_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fee',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='fee',
            name='level',
        ),
        migrations.CreateModel(
            name='FeeAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.level')),
            ],
        ),
    ]
