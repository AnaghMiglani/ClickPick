import { useState, useEffect } from "react";
import { X } from "lucide-react";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "sonner";

interface Product {
  id: string;
  name: string;
  paperType: string;
  pricePerUnit: string;
  color: string;
  paperQuality: string;
  available: boolean;
}

interface ProductEditSidebarProps {
  product: Product | null;
  isOpen: boolean;
  onClose: () => void;
  onSave: (product: Omit<Product, "id" | "available">) => void;
}

export const ProductEditSidebar = ({ product, isOpen, onClose, onSave }: ProductEditSidebarProps) => {
  const [formData, setFormData] = useState({
    name: "",
    paperType: "A4",
    pricePerUnit: "",
    color: "Black & White",
    paperQuality: "basic",
  });

  useEffect(() => {
    if (product) {
      setFormData({
        name: product.name,
        paperType: product.paperType,
        pricePerUnit: product.pricePerUnit.replace("$", ""),
        color: product.color,
        paperQuality: product.paperQuality,
      });
    } else {
      setFormData({
        name: "",
        paperType: "A4",
        pricePerUnit: "",
        color: "Black & White",
        paperQuality: "basic",
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
      paperType: formData.paperType,
      pricePerUnit: `$${formData.pricePerUnit}`,
      color: formData.color,
      paperQuality: formData.paperQuality,
    });

    toast.success(product ? "Product updated successfully" : "Product added successfully");
    onClose();
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
            <Label htmlFor="name">Service Name *</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="e.g., Black & White Printing"
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="paperType">Paper Type</Label>
            <Select
              value={formData.paperType}
              onValueChange={(value) => setFormData({ ...formData, paperType: value })}
            >
              <SelectTrigger id="paperType">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="A4">A4</SelectItem>
                <SelectItem value="A3">A3</SelectItem>
                <SelectItem value="Custom">Custom</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="price">Price *</Label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">$</span>
              <Input
                id="price"
                type="number"
                step="0.01"
                min="0"
                value={formData.pricePerUnit}
                onChange={(e) => setFormData({ ...formData, pricePerUnit: e.target.value })}
                placeholder="0.00"
                className="pl-7"
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="color">Color</Label>
            <Select
              value={formData.color}
              onValueChange={(value) => setFormData({ ...formData, color: value })}
            >
              <SelectTrigger id="color">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Black & White">Black & White</SelectItem>
                <SelectItem value="Colored">Colored</SelectItem>
                <SelectItem value="Custom">Custom</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="paperQuality">Paper Quality</Label>
            <Select
              value={formData.paperQuality}
              onValueChange={(value) => setFormData({ ...formData, paperQuality: value })}
            >
              <SelectTrigger id="paperQuality">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="basic">Basic</SelectItem>
                <SelectItem value="glossy">Glossy</SelectItem>
                <SelectItem value="hardbook">Hardbook</SelectItem>
                <SelectItem value="custom">Custom</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="flex gap-3 pt-4">
            <Button type="submit" className="flex-1">
              {product ? "Save Changes" : "Add Product"}
            </Button>
            <Button type="button" variant="outline" onClick={onClose} className="flex-1">
              Cancel
            </Button>
          </div>
        </form>
      </SheetContent>
    </Sheet>
  );
};
