class ActiveOrderItem {
  final int id;
  final String itemName;
  final String itemImage;
  final int quantity;
  final double cost;
  final String status; // assuming you might add this to the backend model later

  ActiveOrderItem({
    required this.id,
    required this.itemName,
    required this.itemImage,
    required this.quantity,
    required this.cost,
    this.status = 'Processing', // Default status for now
  });

  // Factory to create object from JSON (for when we connect to real backend)
  factory ActiveOrderItem.fromJson(Map<String, dynamic> json) {
    return ActiveOrderItem(
      id: json['id'] ?? 0,
      itemName: json['item_name'] ?? 'Unknown Item',
      // Helper to handle partial or full URLs if needed later
      itemImage: json['item_display_image'] ?? '',
      quantity: json['quantity'] ?? 1,
      cost: (json['cost'] ?? 0).toDouble(),
      status: json['status'] ?? 'Processing',
    );
  }
}