# Generated by Django 4.0.3 on 2022-04-12 07:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.CharField(max_length=100)),
                ('emp_name', models.CharField(max_length=200)),
                ('emp_desi', models.CharField(max_length=200)),
                ('emp_rm1', models.CharField(max_length=200)),
                ('emp_rm1_id', models.CharField(max_length=30)),
                ('emp_rm2', models.CharField(max_length=200)),
                ('emp_rm2_id', models.CharField(max_length=30)),
                ('emp_rm3', models.CharField(max_length=200)),
                ('emp_rm3_id', models.CharField(max_length=30)),
                ('emp_process', models.CharField(max_length=200)),
                ('emp_process_id', models.CharField(max_length=10)),
                ('pc', models.BooleanField(default=False)),
                ('img', models.ImageField(default='user_images/user.png', upload_to='user_images')),
                ('doj', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('on_id', models.IntegerField(blank=True, null=True)),
                ('agent_status', models.CharField(default='Active', max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
