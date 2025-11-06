import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:clickpic/constants/colors.dart';
import 'package:clickpic/models/active_order.dart'; // Re-use this model
import 'package:clickpic/service/api_service.dart';

class OrderHistoryScreen extends StatefulWidget {
  const OrderHistoryScreen({super.key});

  @override
  State<OrderHistoryScreen> createState() => _OrderHistoryScreenState();
}

class _OrderHistoryScreenState extends State<OrderHistoryScreen> {
  final ApiService _apiService = ApiService();
  late Future<List<ActiveOrderItem>> _pastOrders;

  @override
  void initState() {
    super.initState();
    _pastOrders = _apiService.fetchPastOrders() as Future<List<ActiveOrderItem>>;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey.shade50,
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text(
          'Past Orders',
          style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold),
        ),
        backgroundColor: Colors.white,
        elevation: 0,
        centerTitle: true,
      ),
      body: FutureBuilder<List<ActiveOrderItem>>(
        future: _pastOrders,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error loading history.'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('No past orders found.'));
          }

          return ListView.separated(
            padding: const EdgeInsets.all(16),
            itemCount: snapshot.data!.length,
            separatorBuilder: (context, index) => const SizedBox(height: 16),
            itemBuilder: (context, index) {
              final item = snapshot.data![index];
              return _buildHistoryCard(item);
            },
          );
        },
      ),
    );
  }

  Widget _buildHistoryCard(ActiveOrderItem item) {
    // We use a placeholder date as your current model doesn't have one.
    // You can add 'created_at' to your ActiveOrderItem model later if needed.
    final dateStr = DateFormat('MMM dd, yyyy').format(DateTime.now());

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.shade200),
      ),
      child: Row(
        children: [
          // Item Image Placeholder
          Container(
            width: 60,
            height: 60,
            decoration: BoxDecoration(
              color: Colors.grey.shade100,
              borderRadius: BorderRadius.circular(8),
            ),
            child: const Icon(Icons.history, color: Colors.grey),
          ),
          const SizedBox(width: 16),
          // Item Details
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  item.itemName,
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                ),
                const SizedBox(height: 4),
                Text(
                  'Qty: ${item.quantity} • $dateStr',
                  style: TextStyle(color: Colors.grey.shade600, fontSize: 14),
                ),
                const SizedBox(height: 8),
                Text(
                  'Completed',
                  style: TextStyle(
                      color: Colors.green.shade700,
                      fontWeight: FontWeight.bold,
                      fontSize: 12),
                ),
              ],
            ),
          ),
          // Price
          Text(
            '₹${item.cost.toStringAsFixed(2)}',
            style: const TextStyle(
                fontWeight: FontWeight.bold, fontSize: 16, color: AppColors.primary),
          ),
        ],
      ),
    );
  }
}