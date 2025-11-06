import { useState, useEffect } from "react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Plus, Search, Pencil } from "lucide-react";
import { toast } from "sonner";
import { ProductEditSidebar } from "@/components/ProductEditSidebar";
import { api, type Item } from "@/lib/api";

interface Product {
  id: string;
  name: string;
  pricePerUnit: string;
  available: boolean;
}

const Products = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [isEditSidebarOpen, setIsEditSidebarOpen] = useState(false);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const items = await api.getItems();
        
        const formattedProducts: Product[] = items.map((item: Item) => ({
          id: String(item.id),
          name: item.item,
          pricePerUnit: `$${parseFloat(item.price).toFixed(2)}`,
          available: item.in_stock,
        }));
        
        setProducts(formattedProducts);
      } catch (error) {
        console.error("Failed to fetch products:", error);
        toast.error("Failed to load products");
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const handleToggleAvailability = async (productId: string) => {
    try {
      await api.toggleItemStock(parseInt(productId));
      
      setProducts(products.map(product => 
        product.id === productId 
          ? { ...product, available: !product.available }
          : product
      ));
      toast.success("Product availability updated");
    } catch (error) {
      console.error("Failed to toggle availability:", error);
      toast.error("Failed to update product availability");
    }
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

  const handleSaveProduct = async (productData: Omit<Product, "id" | "available">) => {
    try {
      if (selectedProduct) {
        await api.updateItem(parseInt(selectedProduct.id), {
          item: productData.name,
          price: productData.pricePerUnit.replace('$', ''),
          in_stock: selectedProduct.available,
        });
        
        setProducts(products.map(p => 
          p.id === selectedProduct.id 
            ? { ...p, ...productData }
            : p
        ));
        toast.success("Product updated successfully");
      } else {
        const response = await api.createItem({
          item: productData.name,
          price: productData.pricePerUnit.replace('$', ''),
          in_stock: true,
        });
        
        const newProduct: Product = {
          id: String(response.item.id),
          ...productData,
          available: true,
        };
        setProducts([...products, newProduct]);
        toast.success("Product added successfully");
      }
    } catch (error) {
      console.error("Failed to save product:", error);
      toast.error(selectedProduct ? "Failed to update product" : "Failed to create product");
    }
  };

  const handleDeleteProduct = async (productId: string) => {
    try {
      await api.deleteItem(parseInt(productId));
      setProducts(products.filter(p => p.id !== productId));
      toast.success("Product deleted successfully");
    } catch (error) {
      console.error("Failed to delete product:", error);
      toast.error("Failed to delete product");
    }
  };

  const filteredProducts = products.filter(product =>
    product.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-muted-foreground">Loading products...</div>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-8">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-foreground">My Products</h1>
          <Button onClick={handleAddProduct} className="gap-2">
            <Plus className="h-4 w-4" />
            Add New Product
          </Button>
        </div>

        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search for your Products"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>

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
        onDelete={handleDeleteProduct}
      />
    </>
  );
};

export default Products;
