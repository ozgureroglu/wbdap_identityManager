# Generated by Django 3.0.4 on 2020-04-18 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identityManager', '0002_imuser_dummy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imuserprofile',
            name='jobTitle',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
