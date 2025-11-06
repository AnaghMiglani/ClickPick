import { useState, useEffect } from "react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowUpDown, Search } from "lucide-react";
import { OrderDetailsSidebar } from "@/components/OrderDetailsSidebar";
import { api, type Order as BackendOrder, type Printout } from "@/lib/api";
import { toast } from "sonner";

interface Order {
  id: string;
  studentName: string;
  status: "New Order" | "In Progress" | "Pending" | "Completed";
  dateOfOrder: string;
  deliveryTime: string;
}

type SortField = "dateOfOrder" | "deliveryTime" | "status";
type SortOrder = "asc" | "desc";

const MyOrders = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedOrderId, setSelectedOrderId] = useState<string | null>(null);
  const [sortField, setSortField] = useState<SortField>("dateOfOrder");
  const [sortOrder, setSortOrder] = useState<SortOrder>("desc");
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      
      const [activeOrders, pastOrders, activePrintouts, pastPrintouts] = await Promise.all([
        api.getAllActiveOrders(),
        api.getAllPastOrders(),
        api.getAllActivePrintouts(),
        api.getAllPastPrintouts(),
      ]);

      const calculateDeliveryTime = (orderTime: string) => {
        const orderDate = new Date(orderTime);
        const now = new Date();
        const diffMinutes = Math.floor((now.getTime() - orderDate.getTime()) / (1000 * 60));
        return `${Math.max(5, diffMinutes)} mins`;
      };

      const formattedOrders: Order[] = [
        ...activeOrders.map((order: BackendOrder) => ({
          id: `#${order.order_id}`,
          studentName: order.user_name,
          status: "New Order" as const,
          dateOfOrder: new Date(order.order_time).toISOString().split('T')[0],
          deliveryTime: calculateDeliveryTime(order.order_time),
        })),
        ...activePrintouts.map((printout: Printout) => ({
          id: `#P${printout.order_id}`,
          studentName: printout.user_name,
          status: "New Order" as const,
          dateOfOrder: new Date(printout.order_time).toISOString().split('T')[0],
          deliveryTime: calculateDeliveryTime(printout.order_time),
        })),
        ...pastOrders.map((order: BackendOrder) => ({
          id: `#${order.order_id}`,
          studentName: order.user_name,
          status: "Completed" as const,
          dateOfOrder: new Date(order.order_time).toISOString().split('T')[0],
          deliveryTime: calculateDeliveryTime(order.order_time),
        })),
        ...pastPrintouts.map((printout: Printout) => ({
          id: `#P${printout.order_id}`,
          studentName: printout.user_name,
          status: "Completed" as const,
          dateOfOrder: new Date(printout.order_time).toISOString().split('T')[0],
          deliveryTime: calculateDeliveryTime(printout.order_time),
        })),
      ];

      setOrders(formattedOrders);
    } catch (error) {
      console.error("Failed to fetch orders:", error);
      toast.error("Failed to load orders");
    } finally {
      setLoading(false);
    }
  };

  const handleOrderComplete = () => {
    fetchOrders();
    toast.success("Order list updated");
  };

  const getStatusVariant = (status: Order["status"]) => {
    switch (status) {
      case "New Order":
        return "bg-[hsl(142,76%,73%)] text-[hsl(142,76%,20%)] border-[hsl(142,76%,73%)] hover:bg-[hsl(142,76%,73%)]";
      case "In Progress":
        return "bg-[hsl(48,96%,68%)] text-[hsl(48,96%,20%)] border-[hsl(48,96%,68%)] hover:bg-[hsl(48,96%,68%)]";
      case "Pending":
        return "bg-[hsl(0,77%,80%)] text-[hsl(0,77%,25%)] border-[hsl(0,77%,80%)] hover:bg-[hsl(0,77%,80%)]";
      case "Completed":
        return "bg-muted text-muted-foreground border-muted hover:bg-muted";
      default:
        return "bg-muted text-muted-foreground border-muted hover:bg-muted";
    }
  };

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortOrder("asc");
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-muted-foreground">Loading orders...</div>
      </div>
    );
  }

  const filteredAndSortedOrders = orders
    .filter(order =>
      order.studentName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      order.id.toLowerCase().includes(searchQuery.toLowerCase())
    )
    .sort((a, b) => {
      let comparison = 0;
      
      if (sortField === "dateOfOrder") {
        comparison = new Date(a.dateOfOrder).getTime() - new Date(b.dateOfOrder).getTime();
      } else if (sortField === "deliveryTime") {
        const timeA = parseInt(a.deliveryTime);
        const timeB = parseInt(b.deliveryTime);
        comparison = timeA - timeB;
      } else if (sortField === "status") {
        comparison = a.status.localeCompare(b.status);
      }

      return sortOrder === "asc" ? comparison : -comparison;
    });

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  return (
    <>
      <div className="space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-foreground">My Orders</h1>
          <p className="text-muted-foreground">View and manage all your orders</p>
        </div>

        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search by Order ID or Student Name"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>

        {/* Orders Table */}
        <div className="rounded-lg border border-border bg-card overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Order ID</TableHead>
                <TableHead>Student Name</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleSort("dateOfOrder")}
                    className="gap-1 hover:bg-transparent p-0"
                  >
                    Date of Order
                    <ArrowUpDown className="h-4 w-4" />
                  </Button>
                </TableHead>
                <TableHead>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleSort("deliveryTime")}
                    className="gap-1 hover:bg-transparent p-0"
                  >
                    Delivery Time
                    <ArrowUpDown className="h-4 w-4" />
                  </Button>
                </TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredAndSortedOrders.map((order) => (
                <TableRow key={order.id} className="hover:bg-muted/50">
                  <TableCell className="font-medium text-primary">{order.id}</TableCell>
                  <TableCell className="text-muted-foreground">{order.studentName}</TableCell>
                  <TableCell>
                    <Badge className={`${getStatusVariant(order.status)} rounded-full px-4 py-1`}>
                      {order.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-muted-foreground">{formatDate(order.dateOfOrder)}</TableCell>
                  <TableCell className="text-muted-foreground">{order.deliveryTime}</TableCell>
                  <TableCell className="text-right">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setSelectedOrderId(order.id)}
                      className="text-primary hover:text-primary hover:bg-transparent"
                    >
                      View Details
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>

      <OrderDetailsSidebar
        orderId={selectedOrderId}
        isOpen={selectedOrderId !== null}
        onClose={() => setSelectedOrderId(null)}
        onOrderComplete={handleOrderComplete}
      />
    </>
  );
};

export default MyOrders;
