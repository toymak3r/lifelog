# Generated by Django 4.2.3 on 2023-11-15 20:26

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentCards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=200)),
                ('limit', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='payment',
            name='resource',
        ),
        migrations.AlterField(
            model_name='payment',
            name='receipt_artifact',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='files/artifacts/'), upload_to=''),
        ),
        migrations.AddField(
            model_name='payment',
            name='method',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='payment.paymentmethod'),
            preserve_default=False,
        ),
    ]
