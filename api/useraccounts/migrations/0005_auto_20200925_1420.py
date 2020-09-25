# Generated by Django 3.1.1 on 2020-09-25 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccounts', '0004_auto_20200925_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_customer',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='role',
        ),
        migrations.AddField(
            model_name='user',
            name='Role',
            field=models.BooleanField(choices=[(1, 'Customer'), (2, 'Restaurent')], default=1),
        ),
    ]
