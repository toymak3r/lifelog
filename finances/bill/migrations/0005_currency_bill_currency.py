# Generated by Django 4.2.3 on 2024-01-07 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0004_alter_bill_due_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=200)),
                ('symbol', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='bill',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bill.currency'),
        ),
    ]