# Generated by Django 3.0.4 on 2020-04-19 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identityManager', '0008_auto_20200419_0558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='country',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
