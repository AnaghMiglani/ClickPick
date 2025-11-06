import { useState, useEffect } from "react";
import { X } from "lucide-react";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";

interface Product {
  id: string;
  name: string;
  pricePerUnit: string;
  available: boolean;
}

interface ProductEditSidebarProps {
  product: Product | null;
  isOpen: boolean;
  onClose: () => void;
  onSave: (product: Omit<Product, "id" | "available">) => void;
  onDelete?: (productId: string) => void;
}

export const ProductEditSidebar = ({ product, isOpen, onClose, onSave, onDelete }: ProductEditSidebarProps) => {
  const [formData, setFormData] = useState({
    name: "",
    pricePerUnit: "",
  });

  useEffect(() => {
    if (product) {
      setFormData({
        name: product.name,
        pricePerUnit: product.pricePerUnit.replace("₹", ""),
      });
    } else {
      setFormData({
        name: "",
        pricePerUnit: "",
      });
    }
  }, [product]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name || !formData.pricePerUnit) {
      toast.error("Please fill in all required fields");
      return;
    }

    onSave({
      name: formData.name,
      pricePerUnit: `₹${formData.pricePerUnit}`,
    });

    onClose();
  };

  const handleDelete = () => {
    if (product && onDelete) {
      if (confirm(`Are you sure you want to delete "${product.name}"?`)) {
        onDelete(product.id);
        onClose();
      }
    }
  };

  return (
    <Sheet open={isOpen} onOpenChange={onClose}>
      <SheetContent side="left" className="w-full sm:w-[540px] overflow-y-auto">
        <SheetHeader className="border-b border-border pb-4">
          <div className="flex items-center justify-between">
            <SheetTitle className="text-2xl font-bold">
              {product ? "Edit Product" : "Add New Product"}
            </SheetTitle>
            <Button variant="ghost" size="icon" onClick={onClose}>
              <X className="h-5 w-5" />
            </Button>
          </div>
        </SheetHeader>

        <form onSubmit={handleSubmit} className="space-y-6 pt-6">
          <div className="space-y-2">
            <Label htmlFor="name">Product/Service Name *</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="e.g., Notebook, Pen, Black & White Printing"
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="price">Price (per unit) *</Label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">₹</span>
              <Input
                id="price"
                type="number"
                step="1"
                min="0"
                value={formData.pricePerUnit}
                onChange={(e) => setFormData({ ...formData, pricePerUnit: e.target.value })}
                placeholder="0"
                className="pl-7"
                required
              />
            </div>
          </div>

          <div className="flex gap-3 pt-4">
            <Button type="submit" className="flex-1">
              {product ? "Save Changes" : "Add Product"}
            </Button>
            <Button type="button" variant="outline" onClick={onClose} className="flex-1">
              Cancel
            </Button>
          </div>
          
          {product && onDelete && (
            <div className="pt-4 border-t border-border">
              <Button 
                type="button" 
                variant="destructive" 
                onClick={handleDelete}
                className="w-full"
              >
                Delete Product
              </Button>
            </div>
          )}
        </form>
      </SheetContent>
    </Sheet>
  );
};
