import logging
import traceback
from datetime import datetime

from django.contrib import admin
from import_export import resources, results
from import_export.admin import ImportExportModelAdmin
from django.utils.encoding import force_text

from .models import NcmCodes, TypeTaxes, BaseUnits, NcmCategories

logger = logging.getLogger(__name__)
# Set default logging handler to avoid "No handler found" warnings.
logger.addHandler(logging.NullHandler())


class BaseUnitsResource(resources.ModelResource):

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

    def check_ipi(self, data):
        try:
            return float(data)
        except:
            return None

    def check_date(self, data):
        if len(data) == 8:
            return datetime.strptime(data, '%d/%m/%y').date()
        else:
            if len(data) == 10:
                return datetime.strptime(data, '%d/%m/%Y').date()
            else:
                return None

    def collect_base_units(self, row):
        """
        BaseUnits Data
        """
        data = {'name_unit': row['Descrição da uTrib'].upper(), 'unit_symbol': row['uTrib'].upper(), 'repr_unit': 1}
        return self.save_data(BaseUnits, data)

    def collect_ncm_categories(self, row):
        """
        NcmCategories Data
        :param row:
        :return row_result:
        """
        data = {
            'pk_ncmcategories': int(row['catNcm']),
            'name_ncmcat': row['Categoria'].upper()
        }
        return self.save_data(NcmCategories, data)

    def collect_ncm_codes(self, row):
        """
        NcmCodes Data
        :param row:
        :return row_result:
        """
        qsUnits = BaseUnits.objects.filter(unit_symbol=row['uTrib'])[0]
        data = {
            'pk_ncmcodes': row['NCM'],
            'fk_ncmcategories_id': int(row['catNcm']),
            'fk_baseunits_id': qsUnits.pk_baseunits,
            'name_ncm': row['Descrição'],
            'flag_ipi': self.check_ipi(row['IPI']),
            'start_date': self.check_date(row['Início da Vigência']),
            'end_date': self.check_date(row['Fim da Vigência']),
        }
        return self.save_data(NcmCodes, data)

    def check_and_save_data(self, row):
        """
        Create or Update data from a Dataframe row
        :param row: a Series from Dataframe'
        :return: row_result: Array with results
        """
        res_arr = []
        res_arr.append(self.collect_base_units(row))
        res_arr.append(self.collect_ncm_categories(row))
        res_arr.append(self.collect_ncm_codes(row))
        return res_arr

    def import_data(
        self,
        dataset,
        dry_run=False,
        raise_errors=False,
        use_transactions=None,
        collect_failed_rows=False,
        **kwargs
    ):
        row_result = self.get_result_class()()
        df = dataset.df
        df['catNcm'] = df.apply(lambda x: x['NCM'][0:2], axis=1)
        df['Descrição'] = df.apply(lambda x: x['Descrição'].replace(x['NCM'] + ' - ', ''), axis=1)
        for index, row in df.iterrows():
            res = self.check_and_save_data(row)
            for result in res:
                if isinstance(result, results.Error):
                    row_result.append_base_error(result)
                else:
                    row_result.append_row_result(result)
        return row_result

    class Meta:
        model = BaseUnits
        headers = ['NCM', 'Categoria', 'Descrição', 'IPI', 'Início da Vigência',
                   'Fim da Vigência', 'uTrib', 'Descrição da uTrib',
                   'GTIN Produção', 'GTIN Homologação', 'Observação', 'catNcm']


class NcmCodesAdmin(ImportExportModelAdmin):
    resource_class = BaseUnitsResource
    list_display = ('pk_ncmcodes', 'fk_ncmcategories', 'fk_baseunits', 'name_ncm')
    list_filter = ('name_ncm', )
    search_fields = ('pk_ncmcodes', 'name_ncm')


class TypeTaxesAdmin(admin.ModelAdmin):
    list_display = ('pk_type_taxes', 'name_tax', 'flag_tax')
    list_filter = ('pk_type_taxes', 'name_tax', 'flag_tax')
    search_fields = ('pk_type_taxes', 'name_tax')


class BaseUnitsAdmin(admin.ModelAdmin):
    list_display = ('name_unit', 'unit_symbol', 'pk_baseunits')
    list_filter = ('name_unit', 'unit_symbol')
    search_fields = ('name_unit', 'unit_symbol')


class NcmCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name_ncmcat', 'pk_ncmcategories')
    list_filter = ('name_ncmcat', )
    search_fields = ('pk_ncmcategories', 'name_ncmcat')

# Register your models here.


admin.site.register(NcmCodes, NcmCodesAdmin)
admin.site.register(TypeTaxes, TypeTaxesAdmin)
admin.site.register(BaseUnits, BaseUnitsAdmin)
admin.site.register(NcmCategories, NcmCategoriesAdmin)
