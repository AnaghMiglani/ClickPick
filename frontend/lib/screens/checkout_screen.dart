import 'package:clickpic/screens/upload_screen.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:razorpay_flutter/razorpay_flutter.dart';
import 'package:clickpic/constants/colors.dart';
import 'package:clickpic/models/print_jon.dart';
import 'package:clickpic/widgets/cart_provider.dart';
import 'package:clickpic/widgets/custom_button.dart';
import 'package:clickpic/widgets/progressstepper.dart';
import 'package:clickpic/screens/orderporcessing_screen.dart';
import 'package:clickpic/widgets/summary_row.dart';
import 'package:clickpic/service/api_service.dart';

class CheckoutScreen extends StatefulWidget {
  const CheckoutScreen({super.key});

  @override
  State<CheckoutScreen> createState() => _CheckoutScreenState();
}

class _CheckoutScreenState extends State<CheckoutScreen> {
  late Razorpay _razorpay;
  bool _isProcessing = false;

  @override
  void initState() {
    super.initState();
    _razorpay = Razorpay();
    _razorpay.on(Razorpay.EVENT_PAYMENT_SUCCESS, _handlePaymentSuccess);
    _razorpay.on(Razorpay.EVENT_PAYMENT_ERROR, _handlePaymentError);
    _razorpay.on(Razorpay.EVENT_EXTERNAL_WALLET, _handleExternalWallet);
  }

  @override
  void dispose() {
    _razorpay.clear();
    super.dispose();
  }

  void _handlePaymentSuccess(PaymentSuccessResponse response) {

    Navigator.pushAndRemoveUntil(
      context,
      MaterialPageRoute(builder: (context) => const OrderProcessingScreen()),
          (route) => false,
    );
  }

  void _handlePaymentError(PaymentFailureResponse response) {
    setState(() {
      _isProcessing = false;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Payment Failed: ${response.message}'),
        backgroundColor: Colors.red,
      ),
    );
  }

  void _handleExternalWallet(ExternalWalletResponse response) {
    // Handle external wallet (like Paytm) if needed
  }

  /// 1. New function to handle the 2-step process: Upload -> Pay
  Future<void> _processOrder(double totalAmount) async {
    setState(() {
      _isProcessing = true;
    });

    final cart = context.read<CartProvider>();
    final apiService = ApiService();

    // Step 1: Upload Files to Backend
    bool uploadSuccess = await apiService.uploadPrintOrders(cart.itemList, totalAmount);

    if (!uploadSuccess) {
      if (mounted) {
        setState(() {
          _isProcessing = false;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Failed to upload order details. Please try again.'),
            backgroundColor: Colors.red,
          ),
        );
      }
      return;
    }

    // Step 2: If upload succeeded, proceed to Payment
    _openCheckout(totalAmount);
  }

  /// 2. Existing function to open Razorpay
  void _openCheckout(double totalAmount) async {
    final apiService = ApiService();
    final orderId = await apiService.createRazorpayOrder(totalAmount);

    if (orderId == null) {
      if (mounted) {
        setState(() {
          _isProcessing = false;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to initialize payment. Please try again.')),
        );
      }
      return;
    }

    var options = {
      'key': 'YOUR_RAZORPAY_KEY_ID', // TODO: Replace with your actual Razorpay Key ID
      'amount': (totalAmount * 100).toInt(), // Amount in paise
      'name': 'ClickPic',
      'order_id': orderId, // Correct key is usually 'order_id', not 'orderid' for standard integration
      'description': 'Print Order',
      'prefill': {
        'contact': '9876543210', // TODO: Use actual user data
        'email': 'user@example.com' // TODO: Use actual user data
      },
      'external': {
        'wallets': ['paytm']
      }
    };

    try {
      _razorpay.open(options);
    } catch (e) {
      debugPrint('Error opening Razorpay: $e');
      if (mounted) {
        setState(() {
          _isProcessing = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final cart = context.watch<CartProvider>();
    final cartItems = cart.itemList;
    final double subtotal = cart.totalPrice;
    final double tax = subtotal * 0.05;
    final double totalAmount = subtotal + tax;

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text('Checkout',
            style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.white,
        elevation: 0,
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const ProgressStepper(currentStep: 2),
            const SizedBox(height: 32),

            const Text('Order Summary',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.grey.shade50,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                children: [
                  if (cartItems.isEmpty)
                    const Padding(
                      padding: EdgeInsets.symmetric(vertical: 8.0),
                      child: Text("Your cart is empty"),
                    )
                  else
                    ...cartItems
                        .map((item) => _buildCartItemRow(item: item))
                        .toList(),
                  const Divider(height: 24),
                  SummaryRow(
                      title: 'Subtotal',
                      amount: '₹${subtotal.toStringAsFixed(2)}'),
                  const SizedBox(height: 8),
                  SummaryRow(
                      title: 'Tax & Fees (5%)',
                      amount: '₹${tax.toStringAsFixed(2)}'),
                  const Divider(height: 24),
                  SummaryRow(
                      title: 'Total',
                      amount: '₹${totalAmount.toStringAsFixed(2)}',
                      isTotal: true),
                ],
              ),
            ),
            const SizedBox(height: 24), // Reduced this space slightly
            SizedBox(
              width: double.infinity,
              height: 50,
              child: OutlinedButton.icon(
                onPressed: () {
                  // Pop back to UploadScreen if it's 2 steps back in the stack
                  Navigator.of(context).popUntil((route) => route.isFirst);
                  // Or if you want to go specifically to upload screen, you might need named routes
                  // For now, popping twice might work depending on your navigation flow:
                  // Navigator.of(context).pop();
                  // Navigator.of(context).pop();
                },
                icon: const Icon(
                    Icons.add_circle_outline, color: AppColors.primary,
                    size: 24),
                label: const Text(
                  'Add More Files',
                  style: TextStyle(
                      color: AppColors.primary, fontWeight: FontWeight.bold),
                ),
                style: OutlinedButton.styleFrom(
                  foregroundColor: AppColors.primary,
                  side: const BorderSide(color: AppColors.primary, width: 1.5),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12.0),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 16),
            _isProcessing
                ? const Center(child: CircularProgressIndicator())
                : CustomButton(
              text: 'Proceed to Pay',
              onTap: () {
                if (cartItems.isNotEmpty) {
                  _processOrder(totalAmount);
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Your cart is empty')),
                  );
                }
              },
            ),
            const SizedBox(height: 30),
          ],
        ),
      ),
    );
  }

  Widget _buildCartItemRow({required PrintJob item}) {
    double basePrice = 50;
    // Simple price logic placeholder - adjust as needed to match your CartProvider logic
    if (item.color == 'Colored') basePrice += 10;
    if (item.pageSize == 'A1') basePrice += 40;
    else if (item.pageSize == 'A2') basePrice += 30;

    final double totalItemPrice = basePrice * item.copies;

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  item.fileName,
                  style: const TextStyle(fontWeight: FontWeight.w500),
                  overflow: TextOverflow.ellipsis,
                ),
                Text(
                  '${item.copies} x ${item.color}, ${item.pageSize}',
                  style: const TextStyle(color: AppColors.gray, fontSize: 12),
                ),
              ],
            ),
          ),
          Text(
            '₹${totalItemPrice.toStringAsFixed(2)}',
            style: const TextStyle(fontWeight: FontWeight.w500),
          ),
        ],
      ),
    );
  }
}