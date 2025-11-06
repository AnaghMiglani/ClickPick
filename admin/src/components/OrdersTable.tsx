import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Eye } from "lucide-react";

interface Order {
  id: string;
  studentName: string;
  status: "Printing" | "Ready for Pickup" | "Completed";
  price: string;
}

interface OrdersTableProps {
  orders: Order[];
  onViewDetails: (orderId: string) => void;
}

export const OrdersTable = ({ orders, onViewDetails }: OrdersTableProps) => {
  const getStatusVariant = (status: Order["status"]) => {
    switch (status) {
      case "Printing":
        return "bg-primary/10 text-primary border-primary/20";
      case "Ready for Pickup":
        return "bg-success/10 text-success border-success/20";
      case "Completed":
        return "bg-muted text-muted-foreground border-border";
      default:
        return "bg-muted text-muted-foreground border-border";
    }
  };

  return (
    <div className="rounded-lg border border-border bg-card">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Order ID</TableHead>
            <TableHead>Student Name</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Price</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {orders.map((order) => (
            <TableRow key={order.id} className="hover:bg-muted/50">
              <TableCell className="font-medium">{order.id}</TableCell>
              <TableCell>{order.studentName}</TableCell>
              <TableCell>
                <Badge className={getStatusVariant(order.status)}>{order.status}</Badge>
              </TableCell>
              <TableCell className="font-medium">{order.price}</TableCell>
              <TableCell className="text-right">
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => onViewDetails(order.id)}
                  className="text-primary hover:text-primary hover:bg-primary/10"
                >
                  <Eye className="mr-2 h-4 w-4" />
                  View Details
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};
