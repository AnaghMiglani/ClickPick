const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const getAuthHeader = (): Record<string, string> => {
  const token = localStorage.getItem("access_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
};

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeader(),
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ error: "Request failed" }));
    throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

export interface Order {
  order_id: number;
  user_id: number | null;
  user_name: string;
  user_email: string;
  item_id: number | null;
  item_name: string;
  quantity: number;
  cost: string;
  custom_message: string;
  order_time: string;
}

export interface Printout {
  order_id: number;
  user_id: number | null;
  user_name: string;
  user_email: string;
  coloured_pages: string;
  black_and_white_pages: string;
  print_on_one_side: boolean;
  cost: string;
  custom_message: string;
  order_time: string;
  has_file: boolean;
  files_count: number;
}

export interface PrintoutFile {
  id: number;
  file_name: string;
  file_size: number;
  uploaded_at: string;
  coloured_pages: string;
  black_and_white_pages: string;
  print_on_one_side: boolean | null;
  total_pages: number;
}

export interface OrderDetails {
  order_id: string | number;
  user_id: number | null;
  user_name: string;
  user_email: string;
  user_number: string;
  item_id: number | null;
  item_name: string;
  item_price: string;
  quantity: number;
  cost: string;
  custom_message: string;
  order_time: string;
  is_completed: boolean;
}

export interface PrintoutDetails {
  order_id: string | number;
  user_id: number | null;
  user_name: string;
  user_email: string;
  user_number: string;
  coloured_pages: string;
  black_and_white_pages: string;
  print_on_one_side: boolean;
  total_pages: number;
  cost: string;
  custom_message: string;
  order_time: string;
  has_file: boolean;
  files: PrintoutFile[];
  files_count: number;
  is_completed: boolean;
}

export interface DashboardStats {
  new_orders_count: number;
  total_revenue_today: number;
  completed_orders_count: number;
  active_orders_count: number;
  active_printouts_count: number;
  total_active_count: number;
}

export interface Item {
  id: number;
  item: string;
  price: string;
  in_stock: boolean;
  display_image: string | null;
}

export const api = {
  getAllActiveOrders: async (): Promise<Order[]> => {
    return fetchAPI<Order[]>("/stationery/admin/all-active-orders/");
  },

  getAllPastOrders: async (): Promise<Order[]> => {
    return fetchAPI<Order[]>("/stationery/admin/all-past-orders/");
  },

  getAllActivePrintouts: async (): Promise<Printout[]> => {
    return fetchAPI<Printout[]>("/stationery/admin/all-active-printouts/");
  },

  getAllPastPrintouts: async (): Promise<Printout[]> => {
    return fetchAPI<Printout[]>("/stationery/admin/all-past-printouts/");
  },

  getDashboardStats: async (): Promise<DashboardStats> => {
    return fetchAPI<DashboardStats>("/stationery/admin/dashboard-stats/");
  },

  getItems: async (): Promise<Item[]> => {
    return fetchAPI<Item[]>("/stationery/item-list/");
  },

  createItem: async (itemData: Partial<Item>): Promise<{ message: string; item: Item }> => {
    return fetchAPI("/stationery/admin/items/", {
      method: "POST",
      body: JSON.stringify(itemData),
    });
  },

  updateItem: async (itemId: number, itemData: Partial<Item>): Promise<{ message: string; item: Item }> => {
    return fetchAPI(`/stationery/admin/items/${itemId}/`, {
      method: "PUT",
      body: JSON.stringify(itemData),
    });
  },

  deleteItem: async (itemId: number): Promise<{ message: string }> => {
    return fetchAPI(`/stationery/admin/items/${itemId}/delete/`, {
      method: "DELETE",
    });
  },

  toggleItemStock: async (itemId: number): Promise<{ message: string; item_id: number; in_stock: boolean }> => {
    return fetchAPI(`/stationery/admin/items/${itemId}/toggle-stock/`, {
      method: "PATCH",
    });
  },

  getOrderDetails: async (orderId: number): Promise<OrderDetails> => {
    return fetchAPI(`/stationery/admin/orders/${orderId}/`);
  },

  getPrintoutDetails: async (orderId: number): Promise<PrintoutDetails> => {
    return fetchAPI(`/stationery/admin/printouts/${orderId}/`);
  },

  completeOrder: async (orderId: number): Promise<{ message: string; order_id: number }> => {
    return fetchAPI(`/stationery/admin/orders/${orderId}/complete/`, {
      method: "POST",
    });
  },

  completePrintout: async (orderId: number): Promise<{ message: string; order_id: number }> => {
    return fetchAPI(`/stationery/admin/printouts/${orderId}/complete/`, {
      method: "POST",
    });
  },

  downloadPrintoutFile: async (orderId: number): Promise<void> => {
    const token = localStorage.getItem("access_token");
    
    if (!token) {
      throw new Error("Not authenticated - please log in again");
    }
    
    const url = `${API_BASE_URL}/stationery/admin/printouts/${orderId}/download/`;
    
    const response = await fetch(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(errorData.detail || `Download failed: ${response.statusText}`);
    }

    const blob = await response.blob();
    const blobUrl = window.URL.createObjectURL(blob);
    
    // Open PDF in new tab
    window.open(blobUrl, '_blank');
    
    // Clean up the blob URL after a short delay to allow the tab to open
    setTimeout(() => {
      window.URL.revokeObjectURL(blobUrl);
    }, 1000);

    //  download logic 
    // const a = document.createElement('a');
    // a.href = blobUrl;
    // a.download = `printout-${orderId}.pdf`;
    // document.body.appendChild(a);
    // a.click();
    // window.URL.revokeObjectURL(blobUrl);
    // document.body.removeChild(a);
  },

  downloadPrintoutFileById: async (fileId: number): Promise<void> => {
    const token = localStorage.getItem("access_token");
    
    if (!token) {
      throw new Error("Not authenticated - please log in again");
    }
    
    const url = `${API_BASE_URL}/stationery/admin/printout-files/${fileId}/download/`;
    
    const response = await fetch(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(errorData.detail || `Download failed: ${response.statusText}`);
    }

    const blob = await response.blob();
    const blobUrl = window.URL.createObjectURL(blob);
    
    // Open PDF in new tab
    window.open(blobUrl, '_blank');
    
    // Clean up the blob URL after a short delay to allow the tab to open
    setTimeout(() => {
      window.URL.revokeObjectURL(blobUrl);
    }, 1000);
  },

  getMyActiveOrders: async (): Promise<Order[]> => {
    return fetchAPI<Order[]>("/stationery/active-orders/");
  },

  getMyPastOrders: async (): Promise<Order[]> => {
    return fetchAPI<Order[]>("/stationery/past-orders/");
  },

  getMyActivePrintouts: async (): Promise<Printout[]> => {
    return fetchAPI<Printout[]>("/stationery/active-printouts/");
  },

  getMyPastPrintouts: async (): Promise<Printout[]> => {
    return fetchAPI<Printout[]>("/stationery/past-printouts/");
  },
};
