# Generated by Django 5.1.1 on 2024-10-13 10:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_feeamount_fee'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterField(
            model_name='payment',
            name='fee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.feeamount'),
        ),
    ]
