from django.db import models


class ProviderToken(models.Model):
    provider_site = models.CharField(max_length=200)
    token = models.CharField(max_length=50)
