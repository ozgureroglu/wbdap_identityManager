# Generated by Django 2.0.2 on 2018-02-07 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identityManager', '0002_auto_20180207_0548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]