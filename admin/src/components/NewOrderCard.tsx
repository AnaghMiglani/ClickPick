import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Clock, DollarSign } from "lucide-react";

interface NewOrderCardProps {
  orderId: string;
  price: string;
  timeAgo: string;
  onAccept: () => void;
}

export const NewOrderCard = ({ orderId, price, timeAgo, onAccept }: NewOrderCardProps) => {
  return (
    <Card className="border-warning/50 bg-pending/5 transition-all hover:shadow-md">
      <CardContent className="flex items-center justify-between p-6">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <h3 className="text-lg font-semibold text-foreground">{orderId}</h3>
            <span className="inline-flex items-center rounded-full bg-pending px-2.5 py-0.5 text-xs font-medium text-pending-foreground">
              New
            </span>
          </div>
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <DollarSign className="h-4 w-4" />
              <span className="font-medium">{price}</span>
            </div>
            <div className="flex items-center gap-1">
              <Clock className="h-4 w-4" />
              <span>{timeAgo}</span>
            </div>
          </div>
        </div>
        <Button 
          onClick={onAccept} 
          className="bg-success hover:bg-success/90 text-success-foreground font-semibold px-6"
        >
          ACCEPT ORDER
        </Button>
      </CardContent>
    </Card>
  );
};
