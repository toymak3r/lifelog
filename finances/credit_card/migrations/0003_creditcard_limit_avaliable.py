# Generated by Django 4.2.3 on 2023-11-15 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit_card', '0002_remove_creditcard_due_date_creditcard_due_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcard',
            name='limit_avaliable',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100),
            preserve_default=False,
        ),
    ]