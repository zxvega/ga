from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.models import LogEntry
from import_export.admin import ExportActionMixin
from admin_auto_filters.filters import AutocompleteFilter
from rangefilter.filters import DateRangeFilterBuilder
from .models import Location, Customer, Vehicle, Brand, State, Sale, Employee, Type, Move, MoveDetail

admin.site.site_header = "Importadora Ejemplo"
admin.site.site_title  = "Importadora Ejemplo"
admin.site.index_title = "Bienvenidos al portal de administración"

# Log

class LogAdmin(ExportActionMixin,admin.ModelAdmin):
    search_fields = ['user__username']
    search_help_text = "Busqueda por Usuario"
    list_display = ('id','content_type','object_repr','action_flag','user','action_time')
    list_filter = ('action_flag','content_type')
    list_per_page = 25

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(LogEntry,LogAdmin)

# Tipo

class TypeFilter(AutocompleteFilter):
    title = 'Tipo'
    field_name = 'type'


class TypeAdmin(ExportActionMixin,admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('id','title', 'created','updated')
    list_per_page = 10

admin.site.register(Type, TypeAdmin)

# Ubicaciones

class LocationFilter(AutocompleteFilter):
    title = 'Ubicacion'
    field_name = 'location'

class LocationAdmin(ExportActionMixin,admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('id','title','active', 'created','updated')
    list_per_page = 10

admin.site.register(Location, LocationAdmin)

# Marcas

class BrandFilter(AutocompleteFilter):
    title='Marca'
    field_name='brand'

class BrandAdmin(ExportActionMixin,admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('id','title', 'created','updated')
    list_per_page = 10

admin.site.register(Brand, BrandAdmin)

# Estado del Vehiculo

class StateFilter(AutocompleteFilter):
    title='Estado'
    field_name='state'

class StateAdmin(ExportActionMixin,admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('id','title', 'created','updated')
    list_per_page = 10

admin.site.register(State, StateAdmin)

# Cliente

class CustomerAdmin(ExportActionMixin,admin.ModelAdmin):
    search_fields = ['name','last_name','document']
    list_display = ('id','name', 'last_name', 'document', 'addres','telephone','created','updated')
    list_per_page = 10

admin.site.register(Customer, CustomerAdmin) 

# Empleados

class EmployeeAdmin(ExportActionMixin,admin.ModelAdmin):
    readonly_fields = ('user','created','updated',)
    search_fields = ['user__username']
    list_display = ('id', 'user','get_first_name','get_last_name')
    list_per_page = 10

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name     

    get_first_name.short_description = 'Nombres'   
    get_last_name.short_description = 'Apellidos'

admin.site.register(Employee, EmployeeAdmin)

# Vehiculo

class ModelFilter(admin.AllValuesFieldListFilter):
    template = "taller/custom_list_filter.html"

class VehicleAdmin(ExportActionMixin,admin.ModelAdmin):
    model=Vehicle
    readonly_fields = ('available','customer','created','updated',)
    search_fields = ['serie']
    list_filter = ('available',('model',ModelFilter),TypeFilter,StateFilter,BrandFilter,LocationFilter)
    list_display = ('id', 'color', 'detail', 'serie', 'model', 'year', 'type','brand','available', 'location','state','customer')
    list_per_page = 10

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        #new_queryset = queryset.filter(available=True)
        #return new_queryset"""
        return queryset

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('location','available','customer','created','updated',)
        else: 
            return ('available','customer','created','updated',)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            queryset = queryset.filter(available=True)
        return queryset, use_distinct
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.resolver_match.func.__name__ == 'add_view':  
            if db_field.name == 'location':
                kwargs["queryset"] = Location.objects.filter(active = True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Vehicle, VehicleAdmin)


# Movimiento

class MoveDetailInline(admin.TabularInline):
    model = MoveDetail
    readonly_fields = ('source_location',)
    autocomplete_fields = ('vehicle',)
    list_per_page = 10
    extra = 0
    min_num = 1

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

class MoveAdmin(ExportActionMixin,admin.ModelAdmin):
    inlines = [MoveDetailInline]
    search_fields = ['destination_location__title']
    search_help_text = "Si existe error al registrar se debe realizar otra operacion en el orden inverso para el vehiculo"
    list_display = ('id', 'applicant','reason','date','destination_location')
    list_filter = (('date',DateRangeFilterBuilder()),)
    list_per_page = 10

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:  
            return ('destination_location',)
        else:  
            return readonly_fields
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.resolver_match.func.__name__ == 'add_view':  
            if db_field.name == 'destination_location':
                kwargs["queryset"] = Location.objects.filter(active = True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
admin.site.register(Move, MoveAdmin)

# Venta

class SaleAdmin(ExportActionMixin,admin.ModelAdmin):
    search_fields = ['customer__name','customer__last_name','vehicle__serie']
    autocomplete_fields = ('vehicle',)
    list_filter = (('date',DateRangeFilterBuilder()),)
    list_display = ('id', 'date', 'customer', 'vehicle', 'created','updated')
    list_per_page = 10
    model = Sale

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.resolver_match.func.__name__ == 'add_view':  
            if db_field.name == 'vehicle':
                kwargs["queryset"] = Vehicle.objects.filter(available = True)
            if db_field.name == 'customer':
                kwargs["queryset"] = Customer.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:  
            return ('customer','vehicle','created','updated',)
        else:  
            return readonly_fields

admin.site.register(Sale, SaleAdmin)




