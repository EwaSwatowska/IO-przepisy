# Register your models here.
from django.contrib import admin

from .models import Miara, SkladnikiwPrzepisach, Przepis, Skladnik

admin.site.register(Skladnik)
admin.site.register(Miara)
admin.site.register(Przepis)
admin.site.register(SkladnikiwPrzepisach)
