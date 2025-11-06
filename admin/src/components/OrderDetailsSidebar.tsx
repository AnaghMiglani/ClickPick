import { useState } from "react";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { FileText, Clock, X } from "lucide-react";
import { toast } from "sonner";

interface OrderDetailsSidebarProps {
  orderId: string | null;
  isOpen: boolean;
  onClose: () => void;
}

export const OrderDetailsSidebar = ({ orderId, isOpen, onClose }: OrderDetailsSidebarProps) => {
  const [status, setStatus] = useState<"Received" | "In Progress" | "Ready for Pickup">("Received");

  // Mock order data
  const orderDetails = {
    id: orderId || "#12A3",
    totalRevenue: "₹144.00",
    receivedTime: "4 mins ago",
    files: [
      "Portrait_of_Lady_El...",
      "Portrait_of_Lady_El...",
      "Portrait_of_Lady_El...",
    ],
    totalPages: 16,
    copies: 1,
    printType: "Black & White (₹2)",
    pagesToPrint: [
      { from: 2, to: 16 },
      { from: 22, to: 32 },
      { from: 61, to: 123 },
    ],
    comments: "Hey, please don't make punch holes in the first 10 sheets!!",
  };

  const handleDownloadFile = () => {
    toast.success("File downloaded successfully");
  };

  const handleMarkReady = () => {
    setStatus("Ready for Pickup");
    toast.success("Order marked as Ready for Pickup");
  };

  const handleReportIssue = async () => {
    try {
      // TODO: Implement backend API call for reporting issues
      toast.success("Issue reported. Customer has been notified and will visit your shop.");
    } catch (error) {
      console.error("Error reporting issue:", error);
      toast.error("Failed to report issue");
    }
  };

  return (
    <Sheet open={isOpen} onOpenChange={onClose}>
      <SheetContent className="w-full sm:max-w-lg overflow-y-auto">
        <SheetHeader className="flex flex-row items-center justify-between">
          <SheetTitle className="text-2xl font-bold">Order Details</SheetTitle>
          <Button variant="ghost" size="icon" onClick={onClose}>
            <X className="h-5 w-5" />
          </Button>
        </SheetHeader>

        <div className="mt-6 space-y-6">
          {/* Order Header */}
          <div className="flex items-start justify-between">
            <div>
              <h3 className="text-xl font-bold">Order {orderDetails.id}</h3>
              <div className="flex items-center gap-2 mt-1 text-sm text-muted-foreground">
                <Clock className="h-4 w-4" />
                <span>Received {orderDetails.receivedTime}</span>
              </div>
            </div>
            <div className="text-right">
              <p className="text-xl font-bold">{orderDetails.totalRevenue}</p>
              <p className="text-sm text-muted-foreground">Total Revenue</p>
            </div>
          </div>

          {/* Current Status */}
          <div className="space-y-2">
            <p className="text-sm font-medium">Current Status</p>
            <Select value={status} onValueChange={(value: any) => setStatus(value)}>
              <SelectTrigger className="w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Received">Received</SelectItem>
                <SelectItem value="In Progress">In Progress</SelectItem>
                <SelectItem value="Ready for Pickup">Ready for Pickup</SelectItem>
              </SelectContent>
            </Select>
            <div className="flex gap-2 mt-3">
              <Button 
                onClick={handleMarkReady}
                className="flex-1 border border-primary text-primary bg-transparent hover:bg-primary/10"
              >
                Mark Ready to Pickup
              </Button>
              <Button 
                onClick={handleReportIssue}
                variant="ghost"
                className="text-destructive hover:text-destructive hover:bg-destructive/10"
              >
                Report Issue
              </Button>
            </div>
          </div>

          <Separator />

          {/* Files shared with you */}
          <div className="space-y-3">
            <h4 className="font-semibold">Files shared with you</h4>
            <div className="flex flex-wrap gap-2">
              {orderDetails.files.map((file, index) => (
                <Badge 
                  key={index}
                  variant="outline"
                  className="px-3 py-2 text-sm font-normal border-primary/30 text-primary bg-primary/5"
                >
                  <FileText className="h-4 w-4 mr-2" />
                  {file}
                </Badge>
              ))}
            </div>
          </div>

          {/* Order Details Grid */}
          <div className="grid grid-cols-3 gap-4">
            <div>
              <p className="text-sm text-muted-foreground">Total Pages</p>
              <p className="text-lg font-bold">{orderDetails.totalPages}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Number of Copies</p>
              <p className="text-lg font-bold">{orderDetails.copies}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Print Type</p>
              <p className="text-lg font-bold">{orderDetails.printType}</p>
            </div>
          </div>

          {/* Pages to Print */}
          <div className="space-y-3">
            <p className="text-sm font-medium">Pages to Print</p>
            <div className="flex flex-wrap gap-2">
              {orderDetails.pagesToPrint.map((range, index) => (
                <div key={index} className="flex items-center gap-2">
                  <div className="border border-border rounded px-3 py-2 text-center min-w-[60px]">
                    <span className="font-medium">{range.from}</span>
                  </div>
                  <span className="text-muted-foreground">to</span>
                  <div className="border border-border rounded px-3 py-2 text-center min-w-[60px]">
                    <span className="font-medium">{range.to}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Comments */}
          <div className="space-y-2">
            <p className="text-sm font-medium">Comments</p>
            <p className="text-sm text-foreground">{orderDetails.comments}</p>
          </div>

          {/* Download Button */}
          <Button 
            onClick={handleDownloadFile}
            className="w-full bg-[hsl(180,100%,25%)] hover:bg-[hsl(180,100%,20%)] text-white font-semibold"
          >
            Download file
          </Button>
        </div>
      </SheetContent>
    </Sheet>
  );
};
