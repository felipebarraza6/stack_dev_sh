"""
Migración inicial para el sistema de notificaciones
"""
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('module', models.CharField(choices=[('banking', 'Banking'), ('payments', 'Payments'), ('quotations', 'Quotations'), ('projects', 'Projects'), ('invoicing', 'Invoicing'), ('support', 'Support'), ('global', 'Global')], max_length=20)),
                ('notification_type', models.CharField(choices=[('email', 'Email'), ('websocket', 'WebSocket'), ('both', 'Email y WebSocket')], default='both', max_length=20)),
                ('subject', models.CharField(max_length=200)),
                ('message_template', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('available_variables', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'verbose_name': 'Notification Template',
                'verbose_name_plural': 'Notification Templates',
                'db_table': 'notifications_template',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('sent', 'Enviada'), ('failed', 'Fallida'), ('read', 'Leída')], default='pending', max_length=20)),
                ('priority', models.CharField(choices=[('low', 'Baja'), ('medium', 'Media'), ('high', 'Alta'), ('urgent', 'Urgente')], default='medium', max_length=20)),
                ('related_model', models.CharField(blank=True, max_length=50)),
                ('related_id', models.IntegerField(blank=True, null=True)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='notifications.notificationtemplate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='users.user')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'db_table': 'notifications_notification',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='NotificationPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('module', models.CharField(choices=[('banking', 'Banking'), ('payments', 'Payments'), ('quotations', 'Quotations'), ('projects', 'Projects'), ('invoicing', 'Invoicing'), ('support', 'Support'), ('global', 'Global')], max_length=20)),
                ('email_enabled', models.BooleanField(default=True)),
                ('websocket_enabled', models.BooleanField(default=True)),
                ('settings', models.JSONField(blank=True, default=dict)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_preferences', to='users.user')),
            ],
            options={
                'verbose_name': 'Notification Preference',
                'verbose_name_plural': 'Notification Preferences',
                'db_table': 'notifications_preference',
            },
        ),
        migrations.CreateModel(
            name='NotificationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('channel', models.CharField(choices=[('email', 'Email'), ('websocket', 'WebSocket')], max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('sent', 'Enviada'), ('failed', 'Fallida'), ('read', 'Leída')], max_length=20)),
                ('sent_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('delivery_data', models.JSONField(blank=True, default=dict)),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='notifications.notification')),
            ],
            options={
                'verbose_name': 'Notification Log',
                'verbose_name_plural': 'Notification Logs',
                'db_table': 'notifications_log',
            },
        ),
        migrations.AddConstraint(
            model_name='notificationtemplate',
            constraint=models.UniqueConstraint(fields=('name', 'module'), name='unique_template_name_module'),
        ),
        migrations.AddConstraint(
            model_name='notificationpreference',
            constraint=models.UniqueConstraint(fields=('user', 'module'), name='unique_user_module_preference'),
        ),
    ] 