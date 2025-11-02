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

class CheckoutScreen extends StatefulWidget {
  const CheckoutScreen({super.key});

  @override
  State<CheckoutScreen> createState() => _CheckoutScreenState();
}

class _CheckoutScreenState extends State<CheckoutScreen> {
  late Razorpay _razorpay;

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
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => const OrderProcessingScreen()),
    );
  }

  void _handlePaymentError(PaymentFailureResponse response) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Payment Failed: ${response.message}'),
        backgroundColor: Colors.red,
      ),
    );
  }

  void _handleExternalWallet(ExternalWalletResponse response) {
  }

  void _openCheckout(String amountInPaise) {
    // TODO:

    var options = {
      'key': 'YOUR_RAZORPAY_KEY_ID', // TODO: Replace with your key
      'amount': amountInPaise,
      'name': 'ClickPic',
      'description': 'Print Order',
      'prefill': {
        'contact': '8888888888', // TODO: Get user's real phone
        'email': 'test.user@example.com' // TODO: Get user's real email
      }
    };

    try {
      _razorpay.open(options);
    } catch (e) {
      debugPrint('Error opening Razorpay: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    final cart = context.watch<CartProvider>();
    final cartItems = cart.itemList;
    final double subtotal = cart.totalPrice;
    final double tax = subtotal * 0.05; // Example 5% tax
    final double totalAmount = subtotal + tax;
    final String totalAmountInPaise = (totalAmount * 100).toStringAsFixed(0);

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
            const ProgressStepper(currentStep: 2), // This is Step 3
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
                  ...cartItems
                      .map((item) => _BuildCartItemRow(item: item))
                      .toList(),
                  const Divider(height: 24),
                  SummaryRow(
                      title: 'Subtotal',
                      amount: '₹${subtotal.toStringAsFixed(2)}'),
                  const SizedBox(height: 8),


                  const SizedBox(height: 8),
                  SummaryRow(
                      title: 'Tax & Fees',
                      amount: '₹${tax.toStringAsFixed(2)}'),
                  const Divider(height: 24),
                  SummaryRow(
                      title: 'Total',
                      amount: '₹${totalAmount.toStringAsFixed(2)}',
                      isTotal: true),
                ],
              ),
            ),
            const SizedBox(height: 245,),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: OutlinedButton.icon(
                onPressed: () {
                  Navigator.of(context).pop();
                  Navigator.of(context).pop();
                },
                icon: const Icon(Icons.add_circle_outline, color: AppColors.primary, size: 24), // <-- Note: 50 is too big for a button icon
                label: const Text(
                  'Add More Files',
                  style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold),
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
            const SizedBox(height:10,),
            CustomButton(
              text: 'Proceed to Pay',
              onTap: () {
                _openCheckout(totalAmountInPaise);
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _BuildCartItemRow({required PrintJob item}) {
    double basePrice = 50;
    if (item.color == 'Colored') basePrice += 10;
    final double totalItemPrice = basePrice * item.copies;

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Expanded(
            child: Text(
              '${item.fileName} (x${item.copies})',
              style: const TextStyle(color: AppColors.gray),
              overflow: TextOverflow.ellipsis,
            ),
          ),
          Text(
            '₹${totalItemPrice.toStringAsFixed(2)}',
            style: const TextStyle(color: AppColors.gray),
          ),
        ],
      ),
    );
  }
}