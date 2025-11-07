
# Student-facing views
from .student_views import (
    GetItemList,
    GetActiveOrders,
    GetPastOrders,
    GetActivePrintouts,
    GetPastPrintouts,
    CreateOrder,
    CreatePrintout,
)

# Utility views
from .utility_views import (
    CostCalculationView,
    FirstPageGenerationView,
    ImageToPdfAPIView,
    ModPdfView,
)

from .admin import (
    AdminGetAllActiveOrders,
    AdminGetAllActivePrintouts,
    AdminGetAllPastOrders,
    AdminGetAllPastPrintouts,
    AdminDashboardStats,
    AdminGetOrderDetails,
    AdminGetPrintoutDetails,
    AdminUpdateItemStock,
    AdminUpdateItem,
    AdminCreateItem,
    AdminDeleteItem,
    AdminCompleteOrder,
    AdminCompletePrintout,
    SecureFileDownload,
    PrintoutFileDownload,
)

__all__ = [
    # Student views
    'GetItemList',
    'GetActiveOrders',
    'GetPastOrders',
    'GetActivePrintouts',
    'GetPastPrintouts',
    'CreateOrder',
    'CreatePrintout',
    
    # Utility views
    'CostCalculationView',
    'FirstPageGenerationView',
    'ImageToPdfAPIView',
    "ModPdfView",
    
    # Admin dashboard views
    'AdminGetAllActiveOrders',
    'AdminGetAllActivePrintouts',
    'AdminGetAllPastOrders',
    'AdminGetAllPastPrintouts',
    'AdminDashboardStats',
    'AdminGetOrderDetails',
    'AdminGetPrintoutDetails',
    
    # Admin inventory views
    'AdminUpdateItemStock',
    'AdminUpdateItem',
    'AdminCreateItem',
    'AdminDeleteItem',
    
    # Admin order management views
    'AdminCompleteOrder',
    'AdminCompletePrintout',
    
    # Admin file access
    'SecureFileDownload',
    'PrintoutFileDownload',
]
