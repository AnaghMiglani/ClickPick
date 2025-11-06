import { useState, useEffect } from "react";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { FileText, Clock, X, Download, Package } from "lucide-react";
import { toast } from "sonner";
import { api, type OrderDetails, type PrintoutDetails } from "@/lib/api";

interface OrderDetailsSidebarProps {
  orderId: string | null;
  isOpen: boolean;
  onClose: () => void;
  onOrderComplete?: () => void;
}

export const OrderDetailsSidebar = ({ orderId, isOpen, onClose, onOrderComplete }: OrderDetailsSidebarProps) => {
  const [orderDetails, setOrderDetails] = useState<OrderDetails | null>(null);
  const [printoutDetails, setPrintoutDetails] = useState<PrintoutDetails | null>(null);
  const [loading, setLoading] = useState(false);
  const [isPrintout, setIsPrintout] = useState(false);

  useEffect(() => {
    if (!orderId || !isOpen) {
      setOrderDetails(null);
      setPrintoutDetails(null);
      return;
    }

    const fetchDetails = async () => {
      try {
        setLoading(true);
        
        const cleanId = orderId.replace('#', '').replace('P', '');
        const numericId = parseInt(cleanId);
        
        if (orderId.includes('P')) {
          setIsPrintout(true);
          const details = await api.getPrintoutDetails(numericId);
          setPrintoutDetails(details);
        } else {
          setIsPrintout(false);
          const details = await api.getOrderDetails(numericId);
          setOrderDetails(details);
        }
      } catch (error) {
        console.error("Failed to fetch order details:", error);
        toast.error("Failed to load order details");
      } finally {
        setLoading(false);
      }
    };

    fetchDetails();
  }, [orderId, isOpen]);

  const handleDownloadFile = () => {
    if (printoutDetails?.file) {
      window.open(printoutDetails.file, '_blank');
      toast.success("File download started");
    } else {
      toast.error("No file available");
    }
  };

  const handleMarkComplete = async () => {
    try {
      const cleanId = orderId?.replace('#', '').replace('P', '') || '';
      const numericId = parseInt(cleanId);

      if (isPrintout) {
        await api.completePrintout(numericId);
        toast.success("Printout order marked as complete");
      } else {
        await api.completeOrder(numericId);
        toast.success("Order marked as complete");
      }
      
      onOrderComplete?.();
      onClose();
    } catch (error) {
      console.error("Failed to complete order:", error);
      toast.error("Failed to complete order");
    }
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 60) return `${diffMins} mins ago`;
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours} hours ago`;
    const diffDays = Math.floor(diffHours / 24);
    return `${diffDays} days ago`;
  };

  const parsePageRange = (pageStr: string): { from: number; to: number }[] => {
    if (!pageStr || pageStr.trim() === '') return [];
    
    const ranges: { from: number; to: number }[] = [];
    const parts = pageStr.split(',');
    
    parts.forEach(part => {
      const trimmed = part.trim();
      if (trimmed.includes('-')) {
        const [from, to] = trimmed.split('-').map(s => parseInt(s.trim()));
        if (!isNaN(from) && !isNaN(to)) {
          ranges.push({ from, to });
        }
      } else {
        const num = parseInt(trimmed);
        if (!isNaN(num)) {
          ranges.push({ from: num, to: num });
        }
      }
    });
    
    return ranges;
  };

  if (loading) {
    return (
      <Sheet open={isOpen} onOpenChange={onClose}>
        <SheetContent className="w-full sm:max-w-lg overflow-y-auto">
          <div className="flex items-center justify-center h-96">
            <div className="text-muted-foreground">Loading order details...</div>
          </div>
        </SheetContent>
      </Sheet>
    );
  }

  if (!orderDetails && !printoutDetails) {
    return null;
  }

  const details = isPrintout ? printoutDetails : orderDetails;
  if (!details) return null;

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
          <div className="flex items-start justify-between">
            <div>
              <h3 className="text-xl font-bold">Order {orderId}</h3>
              <div className="flex items-center gap-2 mt-1 text-sm text-muted-foreground">
                <Clock className="h-4 w-4" />
                <span>Received {formatTime(details.order_time)}</span>
              </div>
              <p className="text-sm text-muted-foreground mt-1">{details.user_name}</p>
              <p className="text-xs text-muted-foreground">{details.user_email}</p>
              {details.user_number && (
                <p className="text-xs text-muted-foreground">{details.user_number}</p>
              )}
            </div>
            <div className="text-right">
              <p className="text-xl font-bold">₹{Math.floor(parseFloat(details.cost))}</p>
              <p className="text-sm text-muted-foreground">Total Revenue</p>
              {details.is_completed && (
                <Badge className="mt-2 bg-green-100 text-green-800 border-green-200">
                  Completed
                </Badge>
              )}
            </div>
          </div>

          {!details.is_completed && (
            <div className="flex gap-2">
              <Button 
                onClick={handleMarkComplete}
                className="flex-1 bg-primary text-primary-foreground hover:bg-primary/90"
              >
                Mark as Complete
              </Button>
            </div>
          )}

          <Separator />

          {isPrintout && printoutDetails ? (
            <>
              {printoutDetails.file && (
                <div className="space-y-3">
                  <h4 className="font-semibold">File</h4>
                  <Badge 
                    variant="outline"
                    className="px-3 py-2 text-sm font-normal border-primary/30 text-primary bg-primary/5 cursor-pointer"
                    onClick={handleDownloadFile}
                  >
                    <FileText className="h-4 w-4 mr-2" />
                    {printoutDetails.file.split('/').pop()}
                  </Badge>
                </div>
              )}

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-muted-foreground">B&W Pages</p>
                  <p className="text-lg font-bold">{printoutDetails.black_and_white_pages || '0'}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Colored Pages</p>
                  <p className="text-lg font-bold">{printoutDetails.coloured_pages || '0'}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Total Pages</p>
                  <p className="text-lg font-bold">{printoutDetails.total_pages}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Print Mode</p>
                  <p className="text-lg font-bold">
                    {printoutDetails.print_on_one_side ? 'One Side' : 'Both Sides'}
                  </p>
                </div>
              </div>

              {(printoutDetails.black_and_white_pages || printoutDetails.coloured_pages) && (
                <div className="space-y-3">
                  <p className="text-sm font-medium">Page Ranges</p>
                  <div className="space-y-2">
                    {printoutDetails.black_and_white_pages && (
                      <div>
                        <p className="text-xs text-muted-foreground mb-1">Black & White</p>
                        <div className="flex flex-wrap gap-2">
                          {parsePageRange(printoutDetails.black_and_white_pages).map((range, index) => (
                            <div key={index} className="flex items-center gap-2">
                              <div className="border border-border rounded px-3 py-2 text-center min-w-[60px]">
                                <span className="font-medium">{range.from}</span>
                              </div>
                              {range.from !== range.to && (
                                <>
                                  <span className="text-muted-foreground">to</span>
                                  <div className="border border-border rounded px-3 py-2 text-center min-w-[60px]">
                                    <span className="font-medium">{range.to}</span>
                                  </div>
                                </>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    {printoutDetails.coloured_pages && (
                      <div>
                        <p className="text-xs text-muted-foreground mb-1">Colored</p>
                        <div className="flex flex-wrap gap-2">
                          {parsePageRange(printoutDetails.coloured_pages).map((range, index) => (
                            <div key={index} className="flex items-center gap-2">
                              <div className="border border-border rounded px-3 py-2 text-center min-w-[60px]">
                                <span className="font-medium">{range.from}</span>
                              </div>
                              {range.from !== range.to && (
                                <>
                                  <span className="text-muted-foreground">to</span>
                                  <div className="border border-border rounded px-3 py-2 text-center min-w-[60px]">
                                    <span className="font-medium">{range.to}</span>
                                  </div>
                                </>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {printoutDetails.custom_message && (
                <div className="space-y-2">
                  <p className="text-sm font-medium">Comments</p>
                  <p className="text-sm text-foreground">{printoutDetails.custom_message}</p>
                </div>
              )}

              {printoutDetails.file && (
                <Button 
                  onClick={handleDownloadFile}
                  className="w-full bg-[hsl(180,100%,25%)] hover:bg-[hsl(180,100%,20%)] text-white font-semibold"
                >
                  <Download className="h-4 w-4 mr-2" />
                  Download File
                </Button>
              )}
            </>
          ) : orderDetails ? (
            <>
              <div className="space-y-3">
                <h4 className="font-semibold flex items-center gap-2">
                  <Package className="h-5 w-5" />
                  Item Details
                </h4>
                <div className="border border-border rounded-lg p-4">
                  <p className="font-semibold text-lg">{orderDetails.item_name}</p>
                  <p className="text-sm text-muted-foreground">₹{Math.floor(parseFloat(orderDetails.item_price))} per unit</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-muted-foreground">Quantity</p>
                  <p className="text-lg font-bold">{orderDetails.quantity}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Unit Price</p>
                  <p className="text-lg font-bold">₹{Math.floor(parseFloat(orderDetails.item_price))}</p>
                </div>
              </div>

              {orderDetails.custom_message && (
                <div className="space-y-2">
                  <p className="text-sm font-medium">Comments</p>
                  <p className="text-sm text-foreground">{orderDetails.custom_message}</p>
                </div>
              )}
            </>
          ) : null}
        </div>
      </SheetContent>
    </Sheet>
  );
};
