from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    flag = models.ImageField()
    iso_code = models.CharField(max_length=3, unique=True)  # ISO Alpha-3 country code
    prefix = models.CharField(max_length=100, unique=True)  # ISO Alpha-3 country code
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ['name']

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('country', 'name')
        verbose_name_plural = 'Cities'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.country.name}"
