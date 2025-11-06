import { useState } from "react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Plus, Search, Pencil } from "lucide-react";
import { toast } from "sonner";
import { ProductEditSidebar } from "@/components/ProductEditSidebar";

interface Product {
  id: string;
  name: string;
  paperType: string;
  pricePerUnit: string;
  color: string;
  paperQuality: string;
  available: boolean;
}

const Products = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [isEditSidebarOpen, setIsEditSidebarOpen] = useState(false);
  const [products, setProducts] = useState<Product[]>([
    { id: "1", name: "Black & White Printing (A4)", paperType: "A4", pricePerUnit: "$0.10", color: "Black & White", paperQuality: "basic", available: true },
    { id: "2", name: "Color Printing (A4)", paperType: "A4", pricePerUnit: "$0.25", color: "Colored", paperQuality: "basic", available: true },
    { id: "3", name: "Black & White Printing (A3)", paperType: "A3", pricePerUnit: "$0.20", color: "Black & White", paperQuality: "basic", available: true },
    { id: "4", name: "Color Printing (A3)", paperType: "A3", pricePerUnit: "$0.50", color: "Colored", paperQuality: "glossy", available: false },
    { id: "5", name: "Spiral Binding", paperType: "Custom", pricePerUnit: "$5.00", color: "Custom", paperQuality: "custom", available: true },
    { id: "6", name: "Laminating (A4)", paperType: "A4", pricePerUnit: "$2.00", color: "Custom", paperQuality: "glossy", available: true },
    { id: "7", name: "Scanning Service", paperType: "Custom", pricePerUnit: "$1.50", color: "Custom", paperQuality: "custom", available: true },
  ]);

  const handleToggleAvailability = (productId: string) => {
    setProducts(products.map(product => 
      product.id === productId 
        ? { ...product, available: !product.available }
        : product
    ));
    toast.success("Product availability updated");
  };

  const handleEditProduct = (productId: string) => {
    const product = products.find(p => p.id === productId);
    if (product) {
      setSelectedProduct(product);
      setIsEditSidebarOpen(true);
    }
  };

  const handleAddProduct = () => {
    setSelectedProduct(null);
    setIsEditSidebarOpen(true);
  };

  const handleSaveProduct = (productData: Omit<Product, "id" | "available">) => {
    if (selectedProduct) {
      setProducts(products.map(p => 
        p.id === selectedProduct.id 
          ? { ...p, ...productData }
          : p
      ));
    } else {
      const newProduct: Product = {
        id: String(products.length + 1),
        ...productData,
        available: true,
      };
      setProducts([...products, newProduct]);
    }
  };

  const filteredProducts = products.filter(product =>
    product.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-foreground">My Products</h1>
          <Button onClick={handleAddProduct} className="gap-2">
            <Plus className="h-4 w-4" />
            Add New Product
          </Button>
        </div>

        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search for your Products"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>

      {/* Products Table */}
      <div className="rounded-lg border border-border bg-card">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Product Name</TableHead>
              <TableHead>Price/Unit</TableHead>
              <TableHead>Availability</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredProducts.map((product) => (
              <TableRow key={product.id} className="hover:bg-muted/50">
                <TableCell className="font-medium">{product.name}</TableCell>
                <TableCell className="text-muted-foreground">{product.pricePerUnit}</TableCell>
                <TableCell>
                  <Switch
                    checked={product.available}
                    onCheckedChange={() => handleToggleAvailability(product.id)}
                  />
                </TableCell>
                <TableCell className="text-right">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleEditProduct(product.id)}
                    className="text-primary hover:text-primary hover:bg-transparent"
                  >
                    <Pencil className="mr-2 h-4 w-4" />
                    Edit Details
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        </div>
      </div>

      <ProductEditSidebar
        product={selectedProduct}
        isOpen={isEditSidebarOpen}
        onClose={() => setIsEditSidebarOpen(false)}
        onSave={handleSaveProduct}
      />
    </>
  );
};

export default Products;
