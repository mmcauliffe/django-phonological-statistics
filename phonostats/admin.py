from .models import PhonoString

from django.contrib import admin

class PhonoStringAdmin(admin.ModelAdmin):
    model = PhonoString
    list_display = ('Transcription','NoStress')

admin.site.register(PhonoString, PhonoStringAdmin)
