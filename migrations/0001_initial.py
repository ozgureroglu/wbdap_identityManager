# Generated by Django 2.0.4 on 2018-05-03 07:22

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompletedProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=30)),
                ('company', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('abbreviation', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, max_length=80, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(blank=True, max_length=50)),
                ('grade', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)])),
                ('startDate', models.DateField(null=True)),
                ('finishDate', models.DateField(null=True)),
                ('activities', models.TextField(blank=True, max_length=250, null=True)),
                ('description', models.TextField(blank=True, max_length=250, null=True)),
                ('degree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_educations', to='identityManager.Degree')),
            ],
        ),
        migrations.CreateModel(
            name='IMGroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.Group')),
                ('description', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=False)),
                ('memberGroups', models.ManyToManyField(blank=True, null=True, related_name='member_groups', to='identityManager.IMGroup')),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='IMRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('memberGroups', models.ManyToManyField(blank=True, related_name='group_roles', to='identityManager.IMGroup')),
            ],
            options={
                'verbose_name': 'IM Role',
                'verbose_name_plural': 'IM Roles',
            },
        ),
        migrations.CreateModel(
            name='IMUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('ss', models.CharField(blank=True, max_length=10)),
            ],
            options={
                'verbose_name': 'IM User',
                'verbose_name_plural': 'IM Users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='IMUserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobTitle', models.CharField(blank=True, max_length=25, null=True)),
                ('dateOfBirth', models.DateField(blank=True, null=True)),
                ('aboutMe', models.TextField(blank=True, max_length=500, null=True)),
                ('address', models.TextField(blank=True, max_length=500, null=True)),
                ('cellularPhone', models.TextField(blank=True, max_length=500, null=True)),
                ('siteUrl', models.URLField(blank=True, max_length=50, null=True)),
                ('company', models.URLField(blank=True, max_length=50, null=True)),
                ('gender', models.NullBooleanField()),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to='identityManager.IMUser')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.Group')),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Families',
                'ordering': ['name'],
            },
            bases=('auth.group',),
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('abbreviation', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, max_length=80, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=60)),
                ('sector', models.CharField(max_length=60)),
                ('location', models.CharField(max_length=60)),
                ('title', models.CharField(choices=[('Other', 'Other'), ('SOFTWARE_ENGINEER', 'Software Engineer'), ('SOFTWARE_TEST_ENGINEER', 'Software Test Engineer'), ('SOFTWARE_ARCHITECT', 'Software Architect'), ('SOFTWARE_DEVELOPER', 'Software Developer'), ('BACHELOR_SCIENCE', 'Bachelor of Science (B.S.)')], default=('Other', 'Other'), max_length=50)),
                ('technology', models.TextField(blank=True, max_length=500)),
                ('startDate', models.DateField(null=True)),
                ('finishDate', models.DateField(null=True)),
                ('description', models.TextField(blank=True, max_length=250, null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='identityManager.IMUserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='imrole',
            name='memberUsers',
            field=models.ManyToManyField(blank=True, related_name='user_roles', to='identityManager.IMUser'),
        ),
        migrations.AddField(
            model_name='imgroup',
            name='memberUsers',
            field=models.ManyToManyField(blank=True, null=True, related_name='member_users', to='identityManager.IMUser'),
        ),
        migrations.AddField(
            model_name='education',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='identityManager.IMUserProfile'),
        ),
        migrations.AddField(
            model_name='education',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schoolin_educations', to='identityManager.School'),
        ),
        migrations.AddField(
            model_name='completedproject',
            name='user',
            field=models.ManyToManyField(related_name='projects', to='identityManager.IMUser'),
        ),
    ]
