# Generated by Django 3.1.1 on 2020-10-07 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0017_payment_discounted_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='myorder',
            name='delivery_status',
            field=models.BooleanField(default=False),
        ),
    ]
