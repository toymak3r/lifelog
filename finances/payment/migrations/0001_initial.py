# Generated by Django 4.2.3 on 2023-07-14 15:31

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('income', '0001_initial'),
        ('bill', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt_artifact', models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='/files/artifacts/'), upload_to='')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill.bill')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='income.income')),
            ],
        ),
    ]