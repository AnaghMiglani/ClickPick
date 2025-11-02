import 'package:clickpic/constants/colors.dart';
import 'package:clickpic/constants/fonts.dart';
import 'package:clickpic/screens/Details_screen.dart';
import 'package:clickpic/screens/home_screen.dart';
import 'package:clickpic/screens/login_screen.dart';
import 'package:clickpic/screens/orderporcessing_screen.dart';
import 'package:clickpic/screens/signup_screen.dart';
import 'package:flutter/material.dart';
import 'package:clickpic/screens/upload_screen.dart';
import 'package:clickpic/widgets/cart_provider.dart';
import 'package:clickpic/screens/home_screen.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (ctx) => CartProvider(),
      child: MaterialApp(
        title: 'ClickPic',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          primaryColor:  AppColors.primary,
        ),
        home: const HomeScreen(),
      ),
    );
  }
}
