from django.contrib import admin
from .models import Provinces, Languages, Cities, Countries

# Register your models here.

admin.site.register(Provinces)
admin.site.register(Languages)
admin.site.register(Cities)
admin.site.register(Countries)
