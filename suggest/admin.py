from django.contrib import admin

import xadmin

from .models import Suggest

# Register your models here.
admin.site.register(Suggest)

class SuggestAdmin:
    model = Suggest
    list_display = ['id', 'description', 'email', 'platform', 'handled','created_at']
    ordering = ['-updated_at']

xadmin.site.register(Suggest, SuggestAdmin)
