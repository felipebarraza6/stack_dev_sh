# Generated by Django 4.0.5 on 2022-06-22 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_alter_interactiondetail_flow_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interactiondetail',
            name='date_medition',
        ),
        migrations.RemoveField(
            model_name='interactiondetail',
            name='measurement_time',
        ),
        migrations.RemoveField(
            model_name='interactiondetail',
            name='project_code',
        ),
        migrations.AddField(
            model_name='interactiondetail',
            name='date_time_medition',
            field=models.DateField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='interactiondetail',
            name='profile_client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.profileclient'),
        ),
    ]
