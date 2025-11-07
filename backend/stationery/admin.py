from django.contrib import admin
from import_export.admin import ExportActionMixin
from django.utils.html import format_html

from . models import ActiveOrders, PastOrders, ActivePrintOuts, PastPrintOuts, Items, PrintoutFile



class ItemsAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['item', 'price', 'in_stock', 'image_preview']
    list_editable = ['in_stock']


class ActiveOrdersAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'item', 'quantity', 'cost', 'custom_message', 'order_time', 'delete_button']
    
    # Overriding get_actions to remove default delete action because we have implemented custom delete
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    # https://stackoverflow.com/questions/62047370/how-to-put-a-button-on-list-page-for-each-row-in-django-admin-page#:~:text=In%20the%20case%20of%20a,protect%20against%20various%20securit%20issues.&text=The%20values%20of%20object.id,get%20inserted%20into%20the%20placeholders.
    def delete_button(self, obj):
        return format_html(
            "<a href='/stationery/delete_active_order/{}' style='display: inline-block; padding: 10px; font-size: 14px; text-align: center; text-decoration: none; background-color: #007bff; color: #ffffff; border: 1px solid #007bff; border-radius: 5px;'>Mark as Past</a>",
            obj.order_id
        )
        
    delete_button.short_description = "Mark order as past"

class ActivePrintoutsAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'FILE', 'cost', 'custom_message', 'order_time', 'delete_button']
    
    # Overriding get_actions to remove default delete action because we have implemented custom delete
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    # https://stackoverflow.com/questions/62047370/how-to-put-a-button-on-list-page-for-each-row-in-django-admin-page#:~:text=In%20the%20case%20of%20a,protect%20against%20various%20securit%20issues.&text=The%20values%20of%20object.id,get%20inserted%20into%20the%20placeholders.
    def delete_button(self, obj):
        return format_html(
            "<a href='/stationery/delete_active_printout/{}' style='display: inline-block; padding: 10px; font-size: 14px; text-align: center; text-decoration: none; background-color: #007bff; color: #ffffff; border: 1px solid #007bff; border-radius: 5px;'>Mark as Past</a>",
            obj.order_id
        )
        
    def FILE(self, obj):
        return format_html("<a href='{url}' target='_blank' style='text-decoration: underline; color: blue;'>{url}</a>", url = obj.file.url if obj.file else '')
        
    delete_button.short_description = "Mark printout as past"


class PastOrdersAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['order_id', 'user', 'item', 'quantity', 'cost', 'custom_message', 'order_time']  
    list_filter = ['item']      
    
    change_list_template = "stationery/orders/report_generate_changelist.html"
    
    # This will disbale add functionality
    def has_add_permission(self, request):
        return False
    
    # This will disable delete functionality
    def has_delete_permission(self, request, obj=None):
        return False
    
    # This will disable change functionality
    def has_change_permission(self, request, obj=None):
        return False

class PastPrintoutsAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'FILE', 'cost', 'custom_message', 'order_time']    
    
    change_list_template = "stationery/printouts/report_generate_changelist.html"
    
    # This will disbale add functionality
    def has_add_permission(self, request):
        return False
    
    # This will disable delete functionality
    def has_delete_permission(self, request, obj=None):
        return False
    
    # This will disable change functionality
    def has_change_permission(self, request, obj=None):
        return False
    
    def FILE(self, obj):
        return format_html("<a href='{url}' target='_blank' style='text-decoration: underline; color: blue;'>{url}</a>", url = obj.file.url if obj.file else '')


class PrintoutFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_printout_id', 'file_name', 'file_size_kb', 'black_and_white_pages', 'coloured_pages', 'print_on_one_side', 'uploaded_at', 'FILE']
    list_filter = ['uploaded_at', 'print_on_one_side']
    search_fields = ['file_name', 'printout_active__order_id', 'printout_past__order_id']
    
    def get_printout_id(self, obj):
        if obj.printout_active:
            return f"Active #{obj.printout_active.order_id}"
        elif obj.printout_past:
            return f"Past #{obj.printout_past.order_id}"
        return "N/A"
    get_printout_id.short_description = "Printout"
    
    def file_size_kb(self, obj):
        return f"{obj.file_size / 1024:.2f} KB" if obj.file_size else "N/A"
    file_size_kb.short_description = "File Size"
    
    def FILE(self, obj):
        if obj.file:
            return format_html(
                "<a href='{url}' target='_blank' style='text-decoration: underline; color: blue;'>View File</a>", 
                url=obj.file.url
            )
        return "No file"
    FILE.short_description = "Download"

 
        
admin.site.register(Items, ItemsAdmin)
admin.site.register(ActiveOrders, ActiveOrdersAdmin)
admin.site.register(PastOrders, PastOrdersAdmin)
admin.site.register(ActivePrintOuts, ActivePrintoutsAdmin)
admin.site.register(PastPrintOuts, PastPrintoutsAdmin)
admin.site.register(PrintoutFile, PrintoutFileAdmin)