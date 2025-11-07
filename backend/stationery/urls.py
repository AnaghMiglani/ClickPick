from django.urls import path
from . import views
from . import admin_utils

urlpatterns = [    
    # get views:
    path('item-list/', views.GetItemList.as_view(), name='get_item_list'),
    path('active-orders/', views.GetActiveOrders.as_view(), name='get_active_orders'),
    path('past-orders/', views.GetPastOrders.as_view(), name='get_past_orders'),
    path('active-printouts/', views.GetActivePrintouts.as_view(), name='get_active_printouts'),
    path('past-printouts/', views.GetPastPrintouts.as_view(), name='get_past_printouts'),
    
    # admin get views:
    path('admin/all-active-orders/', views.AdminGetAllActiveOrders.as_view(), name='admin_all_active_orders'),
    path('admin/all-past-orders/', views.AdminGetAllPastOrders.as_view(), name='admin_all_past_orders'),
    path('admin/all-active-printouts/', views.AdminGetAllActivePrintouts.as_view(), name='admin_all_active_printouts'),
    path('admin/all-past-printouts/', views.AdminGetAllPastPrintouts.as_view(), name='admin_all_past_printouts'),
    path('admin/dashboard-stats/', views.AdminDashboardStats.as_view(), name='admin_dashboard_stats'),
    
    # admin inventory management:
    path('admin/items/', views.AdminCreateItem.as_view(), name='admin_create_item'),
    path('admin/items/<int:item_id>/', views.AdminUpdateItem.as_view(), name='admin_update_item'),
    path('admin/items/<int:item_id>/delete/', views.AdminDeleteItem.as_view(), name='admin_delete_item'),
    path('admin/items/<int:item_id>/toggle-stock/', views.AdminUpdateItemStock.as_view(), name='admin_toggle_stock'),
    
    # admin order management:
    path('admin/orders/<int:order_id>/', views.AdminGetOrderDetails.as_view(), name='admin_order_details'),
    path('admin/orders/<int:order_id>/complete/', views.AdminCompleteOrder.as_view(), name='admin_complete_order'),
    path('admin/printouts/<int:order_id>/', views.AdminGetPrintoutDetails.as_view(), name='admin_printout_details'),
    path('admin/printouts/<int:order_id>/complete/', views.AdminCompletePrintout.as_view(), name='admin_complete_printout'),
    path('admin/printouts/<int:order_id>/download/', views.SecureFileDownload.as_view(), name='admin_download_file'),
    path('admin/printout-files/<int:file_id>/download/', views.PrintoutFileDownload.as_view(), name='admin_download_printout_file'),
    
    # post views:
    path('create-order/', views.CreateOrder.as_view(), name='create_order'),
    path('create-printout/', views.CreatePrintout.as_view(), name='create_printout'),
    path('calculate-cost/', views.CostCalculationView.as_view(), name='calculate_cost'),
    path('generate-firstpage/', views.FirstPageGenerationView.as_view(), name='generate_firstpage'),
    path('img-to-pdf/', views.ImageToPdfAPIView.as_view(), name='img_to_pdf'),
    # admin panel deletion relaed views :
    path('delete_active_order/<int:order_id>/', admin_utils.delete_active_order, name='delete_active_order'),
    path('delete_active_printout/<int:order_id>/', admin_utils.delete_active_printout, name='delete_active_printout'),
    # admin panel 'report-generation of Orders' related views :
    path('order-reports/<str:duration>/', admin_utils.generate_order_report, name='generate_order_report'),
    path('generate_custom_order_report/', admin_utils.generate_custom_order_report, name='generate_custom_order_report'),
    # admin panel 'report-generation of Printouts' related views :
    path('printout-reports/<str:duration>/', admin_utils.generate_printout_report, name='generate_printout_report'),
    path('generate_custom_printout_report/', admin_utils.generate_custom_printout_report, name='generate_custom_printout_report'),
]