# Generated by Django 4.2.3 on 2023-11-15 21:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0002_alter_bill_artifact'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='due_day',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(31)]),
            preserve_default=False,
        ),
    ]
