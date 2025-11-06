import { useState, useEffect } from "react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Plus, Search, Pencil } from "lucide-react";
import { toast } from "sonner";
import { ProductEditSidebar } from "@/components/ProductEditSidebar";
import { api, type Item } from "@/lib/api";

interface InventoryItem {
  id: string;
  name: string;
  pricePerUnit: string;
  available: boolean;
}

const Products = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedItem, setSelectedItem] = useState<InventoryItem | null>(null);
  const [isEditSidebarOpen, setIsEditSidebarOpen] = useState(false);
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        setLoading(true);
        const items = await api.getItems();
        
        const formattedInventory: InventoryItem[] = items.map((item: Item) => ({
          id: String(item.id),
          name: item.item,
          pricePerUnit: `₹${Math.floor(parseFloat(item.price))}`,
          available: item.in_stock,
        }));
        
        setInventory(formattedInventory);
      } catch (error) {
        console.error("Failed to fetch inventory:", error);
        toast.error("Failed to load inventory");
      } finally {
        setLoading(false);
      }
    };

    fetchInventory();
  }, []);

  const handleToggleAvailability = async (itemId: string) => {
    try {
      await api.toggleItemStock(parseInt(itemId));
      
      setInventory(inventory.map(item => 
        item.id === itemId 
          ? { ...item, available: !item.available }
          : item
      ));
      toast.success("Item availability updated");
    } catch (error) {
      console.error("Failed to toggle availability:", error);
      toast.error("Failed to update item availability");
    }
  };

  const handleEditItem = (itemId: string) => {
    const item = inventory.find(p => p.id === itemId);
    if (item) {
      setSelectedItem(item);
      setIsEditSidebarOpen(true);
    }
  };

  const handleAddItem = () => {
    setSelectedItem(null);
    setIsEditSidebarOpen(true);
  };

  const handleSaveItem = async (itemData: Omit<InventoryItem, "id" | "available">) => {
    try {
      if (selectedItem) {
        await api.updateItem(parseInt(selectedItem.id), {
          item: itemData.name,
          price: itemData.pricePerUnit.replace('₹', ''),
          in_stock: selectedItem.available,
        });
        
        setInventory(inventory.map(p => 
          p.id === selectedItem.id 
            ? { ...p, ...itemData }
            : p
        ));
        toast.success("Item updated successfully");
      } else {
        const response = await api.createItem({
          item: itemData.name,
          price: itemData.pricePerUnit.replace('₹', ''),
          in_stock: true,
        });
        
        const newItem: InventoryItem = {
          id: String(response.item.id),
          ...itemData,
          available: true,
        };
        setInventory([...inventory, newItem]);
        toast.success("Item added successfully");
      }
    } catch (error) {
      console.error("Failed to save item:", error);
      toast.error(selectedItem ? "Failed to update item" : "Failed to create item");
    }
  };

  const handleDeleteItem = async (itemId: string) => {
    try {
      await api.deleteItem(parseInt(itemId));
      setInventory(inventory.filter(p => p.id !== itemId));
      toast.success("Item deleted successfully");
    } catch (error) {
      console.error("Failed to delete item:", error);
      toast.error("Failed to delete item");
    }
  };

  const filteredInventory = inventory.filter(item =>
    item.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-muted-foreground">Loading inventory...</div>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-8">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-foreground">My Inventory</h1>
          <Button onClick={handleAddItem} className="gap-2">
            <Plus className="h-4 w-4" />
            Add New Item
          </Button>
        </div>

        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search inventory"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>

        <div className="rounded-lg border border-border bg-card">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Item Name</TableHead>
                <TableHead>Price/Unit</TableHead>
                <TableHead>Availability</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredInventory.map((item) => (
                <TableRow key={item.id} className="hover:bg-muted/50">
                  <TableCell className="font-medium">{item.name}</TableCell>
                  <TableCell className="text-muted-foreground">{item.pricePerUnit}</TableCell>
                  <TableCell>
                    <Switch
                      checked={item.available}
                      onCheckedChange={() => handleToggleAvailability(item.id)}
                    />
                  </TableCell>
                  <TableCell className="text-right">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleEditItem(item.id)}
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
        product={selectedItem}
        isOpen={isEditSidebarOpen}
        onClose={() => setIsEditSidebarOpen(false)}
        onSave={handleSaveItem}
        onDelete={handleDeleteItem}
      />
    </>
  );
};

export default Products;
