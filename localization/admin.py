from django.contrib import admin
from .models import States, Languages, Cities, Countries

# Register your models here.


class CountriesAdmin(admin.ModelAdmin):
    list_display = ('name_country', 'pk_countries', 'name_country', 'country_symbol')
    list_filter = ('name_country', )
    search_fields = ('name_country', )


class StatesAdmin(admin.ModelAdmin):
    readonly_fields = ('pk_states', 'kc_cities')
    list_display = ('fk_countries', 'state_symbol', 'name_state', 'time_zone')
    list_filter = ('name_state', )
    search_fields = ('name_state', 'state_symbol')

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('pk_states', 'kc_cities')
        form = super(StatesAdmin, self).get_form(request, obj, **kwargs)
        return form


class CitiesAdmin(admin.ModelAdmin):
    readonly_fields = ('pk_cities', )
    list_display = ('name_city', 'zip_code', 'fk_states')
    list_filter = ('name_city', 'zip_code', 'fk_states')
    search_fields = ('name_city', 'zip_code')

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('pk_cities', )
        form = super(CitiesAdmin, self).get_form(request, obj, **kwargs)
        return form


admin.site.register(Languages)
admin.site.register(Countries, CountriesAdmin)
admin.site.register(States, StatesAdmin)
admin.site.register(Cities, CitiesAdmin)
