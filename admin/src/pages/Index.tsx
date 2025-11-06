import { useState, useEffect } from "react";
import { ShoppingBag, TrendingUp, CheckCircle2 } from "lucide-react";
import { KPICard } from "@/components/KPICard";
import { AllOrdersTable } from "@/components/AllOrdersTable";
import { OrderDetailsSidebar } from "@/components/OrderDetailsSidebar";
import { api, type Order, type Printout } from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";
import { useToast } from "@/hooks/use-toast";

const Index = () => {
  const [selectedOrderId, setSelectedOrderId] = useState<string | null>(null);
  const [readOrders, setReadOrders] = useState<Set<string>>(new Set());
  const [allOrders, setAllOrders] = useState<Array<{
    id: string;
    studentName: string;
    status: "New Order" | "In Progress" | "Pending" | "Completed";
    timeOfOrder: string;
  }>>([]);
  const [stats, setStats] = useState({
    newOrdersCount: 0,
    totalRevenue: 0,
    completedOrdersCount: 0,
  });
  const [loading, setLoading] = useState(true);
  
  const { user } = useAuth();
  const { toast } = useToast();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch dashboard stats and all orders in parallel
        const [statsData, ordersData, printoutsData] = await Promise.all([
          api.getDashboardStats(),
          api.getAllActiveOrders(),
          api.getAllActivePrintouts(),
        ]);

        // Update stats
        setStats({
          newOrdersCount: statsData.new_orders_count,
          totalRevenue: statsData.total_revenue_today,
          completedOrdersCount: statsData.completed_orders_count,
        });

        // Combine orders and printouts, convert to display format
        const formattedOrders = [
          ...ordersData.map((order: Order) => ({
            id: `#${order.order_id}`,
            studentName: order.user_name,
            status: "New Order" as const, // Backend doesn't have status yet
            timeOfOrder: new Date(order.order_time).toLocaleTimeString('en-US', { 
              hour: '2-digit', 
              minute: '2-digit',
              hour12: true 
            }),
          })),
          ...printoutsData.map((printout: Printout) => ({
            id: `#P${printout.order_id}`,
            studentName: printout.user_name,
            status: "New Order" as const,
            timeOfOrder: new Date(printout.order_time).toLocaleTimeString('en-US', { 
              hour: '2-digit', 
              minute: '2-digit',
              hour12: true 
            }),
          })),
        ];

        // Sort by order ID (most recent first)
        formattedOrders.sort((a, b) => b.id.localeCompare(a.id));

        setAllOrders(formattedOrders);
      } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
        toast({
          title: "Error",
          description: error instanceof Error ? error.message : "Failed to load dashboard data",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [toast]);

  const handleViewOrder = (orderId: string) => {
    setSelectedOrderId(orderId);
    setReadOrders(prev => new Set(prev).add(orderId));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-muted-foreground">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-foreground">
            Welcome Back {user?.name || 'Admin'}!
          </h1>
        </div>

        {/* KPI Cards */}
        <div className="grid gap-6 md:grid-cols-3">
          <KPICard
            title="New Orders"
            value={stats.newOrdersCount}
            icon={ShoppingBag}
            variant="warning"
          />
          <KPICard
            title="Total Revenue Today"
            value={`₹${Math.floor(stats.totalRevenue)}`}
            icon={TrendingUp}
            variant="success"
          />
          <KPICard
            title="Orders Completed"
            value={stats.completedOrdersCount.toString()}
            icon={CheckCircle2}
            variant="primary"
          />
        </div>

        {/* All Orders Today Section */}
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-foreground">All Orders Today</h2>
          <AllOrdersTable orders={allOrders} onViewOrder={handleViewOrder} readOrders={readOrders} />
        </div>
      </div>

      {/* Order Details Sidebar */}
      <OrderDetailsSidebar
        orderId={selectedOrderId}
        isOpen={selectedOrderId !== null}
        onClose={() => setSelectedOrderId(null)}
      />
    </>
  );
};

export default Index;
