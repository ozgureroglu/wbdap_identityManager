# Generated by Django 3.0.4 on 2020-04-19 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identityManager', '0005_auto_20200419_0224'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]
