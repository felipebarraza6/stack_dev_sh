# Generated by Django 4.2.4 on 2023-08-19 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0069_profileclient_password_dga_software_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileclient',
            name='standard',
            field=models.CharField(blank=True, choices=[('MAYOR', 'mayor'), ('MEDIO', 'medio'), ('MENOR', 'menor'), ('CAUDALES_MUY_PEQUENOS', 'caudales_muy_pequenos')], max_length=300, null=True),
        ),
    ]
