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
  coloured_pages: number;
  black_and_white_pages: number;
  print_on_one_side: boolean;
  cost: string;
  custom_message: string;
  order_time: string;
  file: string | null;
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

  getOrderDetails: async (orderId: number): Promise<any> => {
    return fetchAPI(`/stationery/admin/orders/${orderId}/`);
  },

  getPrintoutDetails: async (orderId: number): Promise<any> => {
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
