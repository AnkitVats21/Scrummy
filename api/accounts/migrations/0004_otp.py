# Generated by Django 3.1.1 on 2020-09-27 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200928_0132'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=6)),
                ('otp_email', models.EmailField(max_length=255)),
                ('time', models.IntegerField()),
            ],
        ),
    ]
