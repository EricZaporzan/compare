from django.contrib import admin

from .models import Comparison

class ComparisonAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "active",)

admin.site.register(Comparison, ComparisonAdmin)
