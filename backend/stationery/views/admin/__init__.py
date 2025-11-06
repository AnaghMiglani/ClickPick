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

__all__ = [
    # Dashboard views
    'AdminGetAllActiveOrders',
    'AdminGetAllActivePrintouts',
    'AdminGetAllPastOrders',
    'AdminGetAllPastPrintouts',
    'AdminDashboardStats',
    'AdminGetOrderDetails',
    'AdminGetPrintoutDetails',
    
    # Inventory views
    'AdminUpdateItemStock',
    'AdminUpdateItem',
    'AdminCreateItem',
    'AdminDeleteItem',
    
    # Order management views
    'AdminCompleteOrder',
    'AdminCompletePrintout',
]
