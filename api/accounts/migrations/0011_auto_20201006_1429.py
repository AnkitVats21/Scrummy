# Generated by Django 3.1.1 on 2020-10-06 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20201004_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='cuisine',
            field=models.CharField(choices=[('North Indian', 'North Indian'), ('South Indian', 'South Indian'), ('Chinese', 'Chinese'), ('Italian', 'Italian'), ('French', 'French'), ('Punjabi', 'Punjabi'), ('Sweets', 'Sweets')], max_length=25),
        ),
    ]
