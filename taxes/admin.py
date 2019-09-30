import logging
import traceback

from django.contrib import admin
from import_export import resources, results
from import_export.admin import ImportExportModelAdmin
from django.utils.encoding import force_text

from .models import Taxes, NcmTaxes
from taxesaux.models import NcmCodes, TypeTaxes

logger = logging.getLogger(__name__)
# Set default logging handler to avoid "No handler found" warnings.
logger.addHandler(logging.NullHandler())


class TaxesResource(resources.ModelResource):

    def fill_logger(self, obj, created, error=None, track=None):
        if error:
            row_result = self.get_error_result_class()(error, track, obj)
        else:
            row_result = self.get_row_result_class()()
            if created:
                row_result.import_type = results.RowResult.IMPORT_TYPE_NEW
            else:
                row_result.import_type = results.RowResult.IMPORT_TYPE_SKIP
            row_result.object_id = obj.pk
            row_result.object_repr = force_text(obj)
        return row_result

    def save_data(self, tb_class, data):
        try:
            obj, created = tb_class.objects.update_or_create(**data)
            row_result = self.fill_logger(obj, created)
        except Exception as e:
            row_result = self.fill_logger(
                obj, created=None, error=e, track=traceback.format_exc()
            )
        return row_result

    def collect_taxes(self, type_tax, origin, destiny, tax):
        data = {
            'fk_type_taxes_id': type_tax,
            'fk_countries_origin_id': 55,
            'fk_countries_destiny_id': 55,
            'fk_states_origin_id': '55.' + origin,
            'fk_states_destiny_id': '55.' + destiny,
            'taxdef': tax
        }
        return self.save_data(Taxes, data)

    def check_and_save_data(self, origin, destiny, tax):
        """
        Create or Update data from a Dataframe row
        :param row: a Series from Dataframe'
        :return: row_result: Array with results
        """
        res_arr = []
        qsTypeTaxes = TypeTaxes.objects.filter(name_tax='ICMS')[0]
        res_arr.append(self.collect_taxes(qsTypeTaxes.pk_type_taxes, origin, destiny, tax))
        return res_arr

    def import_data(self, dataset, dry_run=False, raise_errors=False, use_transactions=None, collect_failed_rows=False, **kwargs):
        row_result = self.get_result_class()()
        df = dataset.df.set_index('TT')
        keys = list(df.keys())
        for row in keys:
            for col in keys:
                tax = float(df[row][col])
                res = self.check_and_save_data(row, col, tax)
                for result in res:
                    if isinstance(result, results.Error):
                        row_result.append_base_error(result)
                    else:
                        row_result.append_row_result(result)
        return row_result

    class Meta:
        model = Taxes
        headers = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
                   'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RN', 'RS',
                   'RJ', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']


class TaxesAdmin(ImportExportModelAdmin):
    resource_class = TaxesResource
    list_display = ('fk_states_origin', 'fk_states_destiny', 'fk_type_taxes', 'taxdef')
    list_filter = ('fk_states_origin', 'fk_states_destiny', 'fk_type_taxes')
    search_fields = ('fk_states_origin', 'fk_states_destiny', 'fk_type_taxes')


class NcmTaxesAdmin(admin.ModelAdmin):
    list_display = ('pk_ncmtaxes', 'fk_taxes', 'fk_ncmcodes', 'tax')
    list_filter = ('fk_taxes',)
    search_fields = ('fk_taxes', 'fk_ncmcodes_id')


admin.site.register(Taxes, TaxesAdmin)
admin.site.register(NcmTaxes, NcmTaxesAdmin)
