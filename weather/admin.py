from django.contrib import admin

from weather.models import City


# Register your models here.

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Admin interface for the City model."""

    list_display = ('name', 'country', 'latitude', 'longitude', 'searched_count')
    search_fields = ('name', 'country')
    list_filter = ('country',)
    ordering = ('name',)

    def has_add_permission(self, request):
        """Disable adding new cities through the admin interface."""
        return False