"""
Admin views module - Contains all admin-facing API endpoints
"""
from .dashboard import (
    AdminGetAllActiveOrders,
    AdminGetAllActivePrintouts,
    AdminGetAllPastOrders,
    AdminGetAllPastPrintouts,
    AdminDashboardStats,
    AdminGetOrderDetails,
    AdminGetPrintoutDetails,
)
from .inventory import (
    AdminUpdateItemStock,
    AdminUpdateItem,
    AdminCreateItem,
    AdminDeleteItem,
)
from .order_management import (
    AdminCompleteOrder,
    AdminCompletePrintout,
)
from .file_access import (
    SecureFileDownload,
)

__all__ = [
    'AdminGetAllActiveOrders',
    'AdminGetAllActivePrintouts',
    'AdminGetAllPastOrders',
    'AdminGetAllPastPrintouts',
    'AdminDashboardStats',
    'AdminGetOrderDetails',
    'AdminGetPrintoutDetails',
    
    'AdminUpdateItemStock',
    'AdminUpdateItem',
    'AdminCreateItem',
    'AdminDeleteItem',
    
    'AdminCompleteOrder',
    'AdminCompletePrintout',
    
    'SecureFileDownload',
]
