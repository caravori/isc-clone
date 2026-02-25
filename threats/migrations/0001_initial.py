# Generated initial migration for threats app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreatLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], max_length=10)),
                ('description', models.TextField()),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-recorded_date'],
            },
        ),
        migrations.CreateModel(
            name='PortActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port_number', models.PositiveIntegerField()),
                ('protocol', models.CharField(choices=[('TCP', 'TCP'), ('UDP', 'UDP')], default='TCP', max_length=10)),
                ('service_name', models.CharField(blank=True, max_length=100)),
                ('scan_count', models.PositiveIntegerField(default=0)),
                ('last_seen', models.DateTimeField(auto_now=True)),
                ('first_seen', models.DateTimeField(auto_now_add=True)),
                ('risk_level', models.CharField(choices=[('low', 'Low Risk'), ('medium', 'Medium Risk'), ('high', 'High Risk'), ('critical', 'Critical Risk')], default='low', max_length=10)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Port Activities',
                'ordering': ['-scan_count'],
            },
        ),
        migrations.CreateModel(
            name='IPReputation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(unique=True)),
                ('reputation', models.CharField(choices=[('clean', 'Clean'), ('suspicious', 'Suspicious'), ('malicious', 'Malicious'), ('blocked', 'Blocked')], default='clean', max_length=20)),
                ('reports_count', models.PositiveIntegerField(default=0)),
                ('first_seen', models.DateTimeField(auto_now_add=True)),
                ('last_seen', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(blank=True, help_text='ISO country code', max_length=2)),
                ('asn', models.PositiveIntegerField(blank=True, help_text='Autonomous System Number', null=True)),
                ('description', models.TextField(blank=True)),
                ('tags', models.CharField(blank=True, help_text='Comma-separated tags', max_length=200)),
            ],
            options={
                'verbose_name': 'IP Reputation',
                'verbose_name_plural': 'IP Reputations',
                'ordering': ['-reports_count', '-last_seen'],
            },
        ),
        migrations.CreateModel(
            name='ThreatIndicator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indicator_type', models.CharField(choices=[('ip', 'IP Address'), ('domain', 'Domain'), ('url', 'URL'), ('hash', 'File Hash'), ('email', 'Email Address'), ('cve', 'CVE')], max_length=10)),
                ('value', models.TextField()),
                ('description', models.TextField()),
                ('severity', models.CharField(choices=[('info', 'Informational'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], default='medium', max_length=10)),
                ('source', models.CharField(blank=True, max_length=200)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('related_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='threat_indicators', to='blog.post')),
            ],
            options={
                'ordering': ['-added_date'],
            },
        ),
        migrations.AddConstraint(
            model_name='portactivity',
            constraint=models.UniqueConstraint(fields=('port_number', 'protocol'), name='threats_portactivity_port_number_protocol_uniq'),
        ),
    ]
