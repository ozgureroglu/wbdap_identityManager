# Generated by Django 2.0.2 on 2018-02-07 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identityManager', '0003_auto_20180207_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='degree',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]