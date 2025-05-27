from django.db import models

# Create your models here.

class City(models.Model):
    """Model representing a city for weather forecasting."""

    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    searched_count = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return f"{self.name}, {self.country}"

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['name']