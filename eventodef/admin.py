from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Evento
# Register your models here.

@admin.register(Evento)
class ViewAdmin(ImportExportModelAdmin):
    pass
