import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:clickpic/constants/colors.dart';
import 'package:clickpic/widgets/cart_provider.dart';
import 'package:clickpic/models/print_jon.dart';
import 'package:clickpic/widgets/custom_button.dart';
import 'package:clickpic/widgets/custom_text_field.dart';
import 'package:clickpic/widgets/progressstepper.dart';
import 'package:clickpic/screens/checkout_screen.dart';

class DetailsScreen extends StatefulWidget {
  const DetailsScreen({super.key});

  @override
  State<DetailsScreen> createState() => _DetailsScreenState();
}

class _DetailsScreenState extends State<DetailsScreen> {
  late CartProvider _cartProvider;
  late List<PrintJob> _cartItems;
  late PrintJob _selectedItem;

  String _selectedColor = 'Black & White';
  String _selectedPageSize = 'A4';
  int _copyCount = 1;
  late TextEditingController _commentController;
  final List<String> _colorOptions = ['Black & White', 'Colored'];
  final List<String> _pageSizeOptions = ['A1', 'A2', 'A3', 'A4', 'A5'];

  @override
  void initState() {
    super.initState();
    _cartProvider = context.read<CartProvider>();
    _cartItems = _cartProvider.itemList;

    _selectedItem = _cartItems.first;

    _loadDetailsForSelectedItem();
  }

  void _loadDetailsForSelectedItem() {
    _copyCount = _selectedItem.copies;
    _selectedColor = _selectedItem.color;
    _selectedPageSize = _selectedItem.pageSize;
    _commentController = TextEditingController(text: _selectedItem.comments);
  }

  void _saveCurrentDetails() {
    final updatedJob = _selectedItem.copyWith(
      copies: _copyCount,
      color: _selectedColor,
      pageSize: _selectedPageSize,
      comments: _commentController.text,
    );
    _cartProvider.updateItem(_selectedItem.id, updatedJob);
  }

  /// Changes the active item and updates the UI
  void _onItemTapped(PrintJob tappedItem) {
    setState(() {
      _selectedItem = tappedItem;
      _loadDetailsForSelectedItem();
    });
  }

  @override
  void dispose() {
    _commentController.dispose();
    super.dispose();
  }

  // --- Copy Counter Methods (Updated) ---
  void _incrementCopies() {
    setState(() {
      _copyCount++;
    });
    _saveCurrentDetails(); // Save on change
  }

  void _decrementCopies() {
    if (_copyCount > 1) {
      setState(() {
        _copyCount--;
      });
      _saveCurrentDetails(); // Save on change
    }
  }

  // --- BUILD METHOD ---
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text(
          'Print Details',
          style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold),
        ),
        backgroundColor: Colors.white,
        elevation: 0,
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const ProgressStepper(currentStep: 1), // This is Step 2
            const SizedBox(height: 24), // Increased spacing

            // --- NEW HORIZONTAL DOCUMENT LIST ---
            const Text(
              'Document',
              style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.black),
            ),
            const SizedBox(height: 12),
            SizedBox(
              height: 80, // Give the list a fixed height
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                itemCount: _cartItems.length,
                itemBuilder: (context, index) {
                  final item = _cartItems[index];
                  final bool isSelected = item.id == _selectedItem.id;

                  return _buildDocumentChip(item, isSelected);
                },
              ),
            ),
            // --- END OF NEW LIST ---

            const SizedBox(height: 24),
            const Text(
              'Comments',
              style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.black),
            ),
            const SizedBox(height: 12),
            CustomTextField(
              controller: _commentController,
              hintText: 'Add special instructions (optional)',
              keyboardType: TextInputType.text,
              width: double.infinity,
            ),
            const SizedBox(height: 24),

            const Text(
              'Options',
              style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.black),
            ),
            const SizedBox(height: 12),
            _buildDropdownRow(
              title: 'Color',
              value: _selectedColor,
              items: _colorOptions,
              onChanged: (newValue) {
                if (newValue != null) {
                  setState(() {
                    _selectedColor = newValue;
                  });
                  _saveCurrentDetails(); // Save on change
                }
              },
            ),
            _buildDropdownRow(
              title: 'Paper Size',
              value: _selectedPageSize,
              items: _pageSizeOptions,
              onChanged: (newValue) {
                if (newValue != null) {
                  setState(() {
                    _selectedPageSize = newValue;
                  });
                  _saveCurrentDetails(); // Save on change
                }
              },
            ),
            _buildCopyCounterRow(),

            const SizedBox(height: 100),
            CustomButton(
              text: 'Proceed to Payment',
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const CheckoutScreen()),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
  Widget _buildDocumentChip(PrintJob item, bool isSelected) {
    return GestureDetector(
      onTap: () => _onItemTapped(item),
      child: Container(
        width: 150, // Fixed width for each item
        margin: const EdgeInsets.only(right: 12),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: isSelected ? AppColors.purple.withOpacity(0.1) : Colors.grey.shade100,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isSelected ? AppColors.purple : Colors.grey.shade300,
            width: 1.5,
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              item.fileName,
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: isSelected ? AppColors.purple : Colors.black,
              ),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            const SizedBox(height: 4),
            Text(
              '${item.copies} Cop(y)ies',
              style: TextStyle(
                fontSize: 12,
                color: isSelected ? AppColors.purple : AppColors.gray,
              ),
            ),
          ],
        ),
      ),
    );
  }

  // (Your _buildDropdownRow and _buildCopyCounterRow methods remain here, unchanged)
  Widget _buildDropdownRow({
    required String title,
    required String value,
    required List<String> items,
    required ValueChanged<String?> onChanged,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            title,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12.0),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(8.0),
              border: Border.all(color: AppColors.Light_gray, width: 1),
            ),
            child: DropdownButtonHideUnderline(
              child: DropdownButton<String>(
                value: value,
                items: items.map((String item) {
                  return DropdownMenuItem<String>(
                    value: item,
                    child: Text(item),
                  );
                }).toList(),
                onChanged: onChanged,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCopyCounterRow() {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          const Text(
            'Copies',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
          ),
          Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(8.0),
              border: Border.all(color: AppColors.Light_gray, width: 1),
            ),
            child: Row(
              children: [
                IconButton(
                  icon: const Icon(Icons.remove),
                  onPressed: _decrementCopies,
                  color: AppColors.gray,
                ),
                Text(
                  '$_copyCount',
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
                IconButton(
                  icon: const Icon(Icons.add),
                  onPressed: _incrementCopies,
                  color: AppColors.primary,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}