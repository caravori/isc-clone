# Generated initial migration for core app

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
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='ISC Clone', max_length=200)),
                ('site_description', models.TextField(blank=True)),
                ('issn', models.CharField(blank=True, help_text='ISSN format: 1234-5678', max_length=9)),
                ('issn_l', models.CharField(blank=True, help_text='Linking ISSN', max_length=9)),
                ('publisher_name', models.CharField(blank=True, max_length=200)),
                ('publisher_country', models.CharField(blank=True, help_text='ISO country code', max_length=2)),
                ('infocon_status', models.CharField(choices=[('green', 'Green - Low threat level'), ('yellow', 'Yellow - Elevated threat level'), ('orange', 'Orange - High threat level'), ('red', 'Red - Severe threat level')], default='green', max_length=10)),
                ('infocon_description', models.TextField(blank=True)),
                ('infocon_updated', models.DateTimeField(auto_now=True)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
            ],
            options={
                'verbose_name': 'Site Settings',
                'verbose_name_plural': 'Site Settings',
            },
        ),
        migrations.CreateModel(
            name='Handler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('expertise', models.CharField(blank=True, max_length=200)),
                ('website', models.URLField(blank=True)),
                ('twitter', models.CharField(blank=True, max_length=100)),
                ('github', models.CharField(blank=True, max_length=100)),
                ('is_active_handler', models.BooleanField(default=True)),
                ('joined_date', models.DateField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__last_name', 'user__first_name'],
            },
        ),
    ]
