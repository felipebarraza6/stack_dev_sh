# Generated by Django 4.0.5 on 2022-07-01 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_quotation_well_technicalinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormLandingContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Fecha de creacion.', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now_add=True, help_text='Fecha de modificacion.', verbose_name='modified at')),
                ('name', models.CharField(blank=True, max_length=1000, null=True)),
                ('phone', models.CharField(blank=True, max_length=1000, null=True)),
                ('email', models.CharField(blank=True, max_length=1000, null=True)),
                ('service', models.CharField(blank=True, max_length=1000, null=True)),
                ('message', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'abstract': False,
            },
        ),
    ]
