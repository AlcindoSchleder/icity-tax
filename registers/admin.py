from django.contrib import admin
from .models import Categories, Registers, RegistersAddress, RegistersCategories

# Register your models here.


class CategoriesAdmin(admin.ModelAdmin):
    readonly_fields = ('pk_categories', )
    list_display = ('name_cat', 'pk_categories', 'flag_tcat', 'flag_repr')
    list_filter = ('name_cat', 'flag_tcat')
    search_fields = ('name_cat', 'flag_tcat')


class RegistersAddressStackedInlineAdmin(admin.StackedInline):
    model = RegistersAddress
    extra = 0
    exclude = ('pk_registers_address', )
    list_fields = ('fk_cities', 'address', 'number', 'quarter', 'zip_code')

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('pk_registers_addresses', )
        form = super(RegistersAddressStackedInlineAdmin, self).get_form(request, obj, **kwargs)
        return form


class RegistersCategoriesItemsInLine(admin.TabularInline):
    model = RegistersCategories
    extra = 0
    list_fields = ('fk_registers', 'fk_categories', 'flag_active', 'insert_date')
    readonly_fields = ('insert_date', )


class RegistersAdmin(admin.ModelAdmin):
    readonly_fields = ('pk_registers', 'kc_registers_address')
    list_display = ('main_doc', 'flag_treg', 'fk_user', 'first_name', 'last_name', 'enterprise_name', 'pk_registers')
    list_filter = ('pk_registers', 'fk_user', 'first_name', 'last_name', 'enterprise_name', 'main_doc')
    search_fields = ('first_name', 'last_name', 'enterprise_name', 'fk_user', 'main_doc')
    inlines = (RegistersAddressStackedInlineAdmin, RegistersCategoriesItemsInLine)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('kc_registers_address', )
        form = super(RegistersAdmin, self).get_form(request, obj, **kwargs)
        return form


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Registers, RegistersAdmin)
# admin.site.register(RegistersAddress, RegistersAddressAdmin)
# admin.site.register(RegistersCategories, RegistersCategoriesAdmin)
