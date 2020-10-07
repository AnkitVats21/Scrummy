# Generated by Django 3.1.1 on 2020-10-06 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_restaurent_wallpaper'),
        ('cart', '0015_payment_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='myorder',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.restaurent'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.restaurent'),
        ),
    ]