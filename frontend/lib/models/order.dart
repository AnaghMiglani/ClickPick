class OrderItem {
  final String itemName;
  final int quantity;
  final double cost;

  OrderItem({required this.itemName, required this.quantity, required this.cost});

  factory OrderItem.fromJson(Map<String, dynamic> json) {
    return OrderItem(
      itemName: json['item_name'] ?? 'Unknown Item',
      quantity: json['quantity'] ?? 0,
      cost: (json['cost'] ?? 0).toDouble(),
    );
  }
}

class Order {
  final int id;
  final String status;
  final DateTime createdAt;
  final double totalCost;
  final List<OrderItem> items;

  Order({
    required this.id,
    required this.status,
    required this.createdAt,
    required this.totalCost,
    required this.items,
  });

  factory Order.fromJson(Map<String, dynamic> json) {
    var list = json['items'] as List? ?? [];
    List<OrderItem> itemsList = list.map((i) => OrderItem.fromJson(i)).toList();

    return Order(
      id: json['id'] ?? 0,
      status: json['status'] ?? 'Completed',
      createdAt: DateTime.tryParse(json['created_at'] ?? '') ?? DateTime.now(),
      totalCost: (json['total_cost'] ?? 0).toDouble(),
      items: itemsList,
    );
  }
}