from django.contrib import admin

# Register your models here.
from .models import Contrib


@admin.register(Contrib)
class ContribAdmin(admin.ModelAdmin):
    search_fields = ["name", "email", "phone"]
    list_display = ("name", "date",)
