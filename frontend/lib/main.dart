import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:clickpic/constants/colors.dart';
import 'package:clickpic/widgets/cart_provider.dart';

// Import all screens
import 'package:clickpic/screens/login_screen.dart';
import 'package:clickpic/screens/signup_screen.dart';
import 'package:clickpic/screens/home_screen.dart';
import 'package:clickpic/screens/upload_screen.dart';
import 'package:clickpic/screens/Details_screen.dart';
import 'package:clickpic/screens/checkout_screen.dart';
import 'package:clickpic/screens/orderporcessing_screen.dart';
import 'package:clickpic/screens/activeorder_screen.dart';
import 'package:clickpic/screens/orderhistory_screen.dart';
// import 'package:clickpic/screens/trackorder_screen.dart'; // If you have this implemented

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => CartProvider()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ClickPic',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primaryColor: AppColors.primary,
        useMaterial3: true,
        scaffoldBackgroundColor: Colors.white,
      ),
      initialRoute: '/login',
      routes: {
        '/login': (context) => const LoginScreen(),
        '/signup': (context) => const SignupScreen(),
        '/home': (context) => const HomeScreen(),
        '/upload': (context) => const UploadScreen(),
        '/details': (context) => const DetailsScreen(),
        '/checkout': (context) => const CheckoutScreen(),
        '/processing': (context) => const OrderProcessingScreen(),
        '/active_orders': (context) => const ActiveOrderScreen(),
        '/order_history': (context) => const OrderHistoryScreen(),
      },
    );
  }
}