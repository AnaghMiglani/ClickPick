import { useState } from "react";
import { ShoppingBag, TrendingUp, CheckCircle2 } from "lucide-react";
import { KPICard } from "@/components/KPICard";
import { AllOrdersTable } from "@/components/AllOrdersTable";
import { OrderDetailsSidebar } from "@/components/OrderDetailsSidebar";

const Index = () => {
  const [selectedOrderId, setSelectedOrderId] = useState<string | null>(null);
  const [readOrders, setReadOrders] = useState<Set<string>>(new Set());

  const allOrders = [
    { id: "#12A3", studentName: "Ansh Kapila", status: "New Order" as const, timeOfOrder: "10:30 AM" },
    { id: "#12A4", studentName: "Rahul Sharma", status: "In Progress" as const, timeOfOrder: "11:45 AM" },
    { id: "#12A5", studentName: "Priya Patel", status: "Pending" as const, timeOfOrder: "01:15 PM" },
    { id: "#12A6", studentName: "Amit Kumar", status: "Completed" as const, timeOfOrder: "09:20 AM" },
  ];

  const handleViewOrder = (orderId: string) => {
    setSelectedOrderId(orderId);
    setReadOrders(prev => new Set(prev).add(orderId));
  };

  return (
    <>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-foreground">Welcome Back Ansh!</h1>
        </div>

        {/* KPI Cards */}
        <div className="grid gap-6 md:grid-cols-3">
          <KPICard
            title="New Orders"
            value={12}
            icon={ShoppingBag}
            variant="warning"
          />
          <KPICard
            title="Total Revenue Today"
            value="$450"
            icon={TrendingUp}
            variant="success"
          />
          <KPICard
            title="Orders Completed"
            value="35"
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
