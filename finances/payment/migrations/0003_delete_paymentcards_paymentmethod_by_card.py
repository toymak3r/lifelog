# Generated by Django 4.2.3 on 2023-11-15 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('credit_card', '0002_remove_creditcard_due_date_creditcard_due_day'),
        ('payment', '0002_paymentcards_paymentmethod_remove_payment_resource_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PaymentCards',
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='by_card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='credit_card.creditcard'),
        ),
    ]