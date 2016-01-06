from django.contrib import admin

from .models import Comparison, ComparisonItem

class ComparisonAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "active",)

class ComparisonItemAdmin(admin.ModelAdmin):
    list_display = ("title", "owner",)

admin.site.register(Comparison, ComparisonAdmin)
admin.site.register(ComparisonItem, ComparisonItemAdmin)
