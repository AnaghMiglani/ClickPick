import 'package:flutter/material.dart';
import 'package:clickpic/constants/colors.dart';
import 'package:clickpic/service/api_service.dart';

class ActiveOrderScreen extends StatefulWidget {
  const ActiveOrderScreen({super.key});

  @override
  State<ActiveOrderScreen> createState() => _ActiveOrderScreenState();
}

class _ActiveOrderScreenState extends State<ActiveOrderScreen> {
  late Future<List<dynamic>> _activeOrdersFuture;

  @override
  void initState() {
    super.initState();
    _activeOrdersFuture = ApiService().fetchActivePrintouts();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Active Orders", style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _activeOrdersFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text("Error loading orders"));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.print_disabled_outlined, size: 64, color: Colors.grey),
                  SizedBox(height: 16),
                  Text("No active print jobs", style: TextStyle(fontSize: 18, color: Colors.grey)),
                ],
              ),
            );
          }

          // If we have data, display it in a list
          final orders = snapshot.data!;
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: orders.length,
            itemBuilder: (context, index) {
              final order = orders[index];
              // Adapt these fields based on your exact API response structure
              return Card(
                elevation: 2,
                margin: const EdgeInsets.only(bottom: 12),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                child: ListTile(
                  leading: Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: AppColors.purple.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Icon(Icons.print, color: AppColors.purple),
                  ),
                  title: Text("Order #${order['id']}", style: const TextStyle(fontWeight: FontWeight.bold)),
                  subtitle: Text("Status: ${order['status'] ?? 'Processing'}"),
                  trailing: Text(
                    "₹${order['cost']}",
                    style: const TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 16),
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}