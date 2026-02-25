"""
Threat intelligence models for ISC Clone.
"""
from django.db import models
from django.contrib.auth.models import User
from blog.models import Post


class ThreatLevel(models.Model):
    """Historical threat level tracking."""
    LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    description = models.TextField()
    recorded_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-recorded_date']
    
    def __str__(self):
        return f'{self.level.upper()} - {self.recorded_date.strftime("%Y-%m-%d %H:%M")}'


class PortActivity(models.Model):
    """Port scanning and activity statistics."""
    port_number = models.PositiveIntegerField()
    protocol = models.CharField(
        max_length=10,
        choices=[('TCP', 'TCP'), ('UDP', 'UDP')],
        default='TCP'
    )
    service_name = models.CharField(max_length=100, blank=True)
    
    # Statistics
    scan_count = models.PositiveIntegerField(default=0)
    last_seen = models.DateTimeField(auto_now=True)
    first_seen = models.DateTimeField(auto_now_add=True)
    
    # Risk assessment
    RISK_CHOICES = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('critical', 'Critical Risk'),
    ]
    risk_level = models.CharField(
        max_length=10,
        choices=RISK_CHOICES,
        default='low'
    )
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-scan_count']
        unique_together = ['port_number', 'protocol']
        verbose_name_plural = 'Port Activities'
    
    def __str__(self):
        return f'Port {self.port_number}/{self.protocol} - {self.service_name or "Unknown"}'


class IPReputation(models.Model):
    """IP address reputation tracking."""
    ip_address = models.GenericIPAddressField(unique=True)
    
    # Classification
    REPUTATION_CHOICES = [
        ('clean', 'Clean'),
        ('suspicious', 'Suspicious'),
        ('malicious', 'Malicious'),
        ('blocked', 'Blocked'),
    ]
    reputation = models.CharField(
        max_length=20,
        choices=REPUTATION_CHOICES,
        default='clean'
    )
    
    # Tracking
    reports_count = models.PositiveIntegerField(default=0)
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    
    # Geographic data
    country = models.CharField(max_length=2, blank=True, help_text='ISO country code')
    asn = models.PositiveIntegerField(null=True, blank=True, help_text='Autonomous System Number')
    
    # Additional info
    description = models.TextField(blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text='Comma-separated tags')
    
    class Meta:
        ordering = ['-reports_count', '-last_seen']
        verbose_name = 'IP Reputation'
        verbose_name_plural = 'IP Reputations'
    
    def __str__(self):
        return f'{self.ip_address} - {self.reputation}'


class ThreatIndicator(models.Model):
    """Indicators of Compromise (IoCs)."""
    IOC_TYPES = [
        ('ip', 'IP Address'),
        ('domain', 'Domain'),
        ('url', 'URL'),
        ('hash', 'File Hash'),
        ('email', 'Email Address'),
        ('cve', 'CVE'),
    ]
    
    indicator_type = models.CharField(max_length=10, choices=IOC_TYPES)
    value = models.TextField()
    description = models.TextField()
    
    # Severity
    SEVERITY_CHOICES = [
        ('info', 'Informational'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    
    # Metadata
    source = models.CharField(max_length=200, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # References
    related_post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='threat_indicators'
    )
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-added_date']
    
    def __str__(self):
        return f'{self.indicator_type.upper()}: {self.value[:50]}'
