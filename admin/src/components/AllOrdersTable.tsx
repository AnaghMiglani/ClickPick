import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

interface Order {
  id: string;
  studentName: string;
  status: "New Order" | "In Progress" | "Pending" | "Completed";
  timeOfOrder: string;
}

interface AllOrdersTableProps {
  orders: Order[];
  onViewOrder: (orderId: string) => void;
  readOrders?: Set<string>;
}

export const AllOrdersTable = ({ orders, onViewOrder, readOrders = new Set() }: AllOrdersTableProps) => {
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

  const getRowBgColor = (orderId: string, status: Order["status"]) => {
    const isUnread = status === "New Order" && !readOrders.has(orderId);
    return isUnread ? "bg-[hsl(200,100%,90%)]" : "bg-background";
  };

  return (
    <div className="rounded-lg border border-border bg-card overflow-hidden">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Order ID</TableHead>
            <TableHead>Student Name</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Time of Order</TableHead>
            <TableHead className="text-right"></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {orders.map((order, index) => (
            <TableRow key={`${order.id}-${index}`} className={`${getRowBgColor(order.id, order.status)} hover:opacity-90`}>
              <TableCell className="font-medium text-primary">{order.id}</TableCell>
              <TableCell className="text-muted-foreground">{order.studentName}</TableCell>
              <TableCell>
                <Badge className={`${getStatusVariant(order.status)} rounded-full px-4 py-1`}>
                  {order.status}
                </Badge>
              </TableCell>
              <TableCell className="text-muted-foreground">{order.timeOfOrder}</TableCell>
              <TableCell className="text-right">
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => onViewOrder(order.id)}
                  className="text-primary hover:text-primary hover:bg-transparent"
                >
                  View Order
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};
