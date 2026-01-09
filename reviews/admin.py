
from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'sentiment', 'created_at')
    list_filter = ('sentiment', 'created_at')
    search_fields = ('text', 'user__username')
