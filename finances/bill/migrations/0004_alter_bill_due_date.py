# Generated by Django 4.2.3 on 2023-11-15 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0003_bill_due_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
