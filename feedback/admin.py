from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('booking', 'customer', 'rating', 'created_at')
    list_filter = ('rating',)

admin.site.register(Feedback, FeedbackAdmin)
