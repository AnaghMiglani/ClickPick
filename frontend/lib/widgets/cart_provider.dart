import 'dart:io';
import 'package:flutter/material.dart';
import 'package:clickpic/models/print_jon.dart'; // Make sure this path is correct

class CartProvider with ChangeNotifier {
  // A Map is efficient for looking up, updating, and removing items by ID.
  final Map<String, PrintJob> _items = {};

  /// Returns a copy of the items map.
  Map<String, PrintJob> get items {
    return {..._items};
  }

  /// Returns a list view of the items, useful for ListView.builder.
  List<PrintJob> get itemList {
    return _items.values.toList();
  }

  /// Adds a new file to the cart.
  void addFile(File file) {
    // Generate a unique ID (a timestamp is simple and effective)
    final id = DateTime.now().toIso8601String();
    // Get the file name from the path
    final fileName = file.path.split('/').last;

    _items.putIfAbsent(
      id,
          () => PrintJob(
        id: id,
        fileName: fileName,
        // You would also store the actual file path or bytes here
        // to upload later.
        // file: file,
      ),
    );

    // This is the most important part:
    // It tells any widgets listening to this provider to rebuild.
    notifyListeners();
  }

  /// Updates an existing item in the cart.
  void updateItem(String id, PrintJob updatedJob) {
    if (_items.containsKey(id)) {
      _items.update(id, (existing) => updatedJob);
      notifyListeners();
    }
  }

  /// Removes an item from the cart using its ID.
  void removeItem(String id) {
    _items.remove(id);
    notifyListeners();
  }

  /// Calculates the total price of all items in the cart.
  double get totalPrice {
    var total = 0.0;

    // Loop through each item and calculate its price
    // TODO: Replace this placeholder logic with your real rules
    _items.forEach((key, job) {
      double itemPrice = 50; // Base price

      // Add extra cost for color
      if (job.color == 'Colored') {
        itemPrice += 10;
      }

      // Add price based on page size
      if (job.pageSize == 'A1') {
        itemPrice += 40;
      } else if (job.pageSize == 'A2') {
        itemPrice += 30;
      }

      total += itemPrice * job.copies;
    });

    return total;
  }
}