import 'package:clickpic/constants/colors.dart';
import 'package:clickpic/screens/signup_screen.dart';
import 'package:clickpic/widgets/country_code_dropdown.dart';
import 'package:clickpic/widgets/custom_button.dart';
import 'package:clickpic/widgets/custom_text_field.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import '../service/api_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _numController = TextEditingController();
  final TextEditingController _pwdController = TextEditingController();
  String _selectedCountryCode = '+91';
  bool _isPasswordVisible = false;

  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      backgroundColor: Colors.white,
      body: Stack(
        children: [
          _buildHeaderImage(screenHeight),
          _buildLoginForm(screenHeight),
        ],
      ),
    );
  }

  Widget _buildHeaderImage(double screenHeight) {
    return Image.asset(
      'assets/images/login_header.png',
      width: double.infinity,
      height: screenHeight * 0.29,
      fit: BoxFit.cover,
    );
  }

  Widget _buildTopIndicator() {
    return Center(
      child: Container(
        width: 54,
        height: 8,
        decoration: BoxDecoration(
          color: const Color(0xFFB3B3B3),
          borderRadius: BorderRadius.circular(8),
        ),
      ),
    );
  }

  Widget _buildLoginForm(double screenHeight) {
    return SingleChildScrollView(
      child: Column(
        children: [
          SizedBox(height: screenHeight * 0.26),
          Container(
            width: double.infinity,
            constraints: BoxConstraints(minHeight: screenHeight * 0.73),
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 32),
            decoration: const BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.vertical(top: Radius.circular(32)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildTopIndicator(),
                const SizedBox(height: 15),
                _buildWelcomeHeader(),
                const SizedBox(height: 15),
                _buildPhoneNumberSection(),
                const SizedBox(height: 20),
                _buildPasswordSection(),
                const SizedBox(height: 20),
                _buildLoginButton(),
                const SizedBox(height: 15),
                _buildBottomSection(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildWelcomeHeader() {
    return const Column(
      children: [
        Center(
          child: Text(
            'Welcome Back!',
            style: TextStyle(
              fontWeight: FontWeight.w700,
              fontSize: 24,
              color: AppColors.primary,
            ),
          ),
        ),
        Center(
          child: Text.rich(
            TextSpan(
              style: TextStyle(fontSize: 12),
              text: 'Please ',
              children: <TextSpan>[
                TextSpan(
                  text: 'Log In',
                  style: TextStyle(
                    color: AppColors.primary,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                TextSpan(text: ' to Continue'),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildPhoneNumberSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildLabel('Phone number'),
        const SizedBox(height: 5),
        Row(
          children: [
            CountryCodeDropdown(
              onChanged: (code) {
                setState(() {
                  _selectedCountryCode = code;
                });
              },
            ),
            const SizedBox(width: 10),
            Expanded(
              child: CustomTextField(
                keyboardType: TextInputType.phone,
                controller: _numController,
                hintText: 'Phone Number',
                width: double.infinity,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildPasswordSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildLabel('Password'),
        const SizedBox(height: 5),
        CustomTextField(
          isObscureText: !_isPasswordVisible,
          keyboardType: TextInputType.text,
          controller: _pwdController,
          hintText: 'Password',
          width: double.infinity,
          suffixIcon: IconButton(
            icon: Icon(
              _isPasswordVisible
                  ? Icons.visibility_outlined
                  : Icons.visibility_off_outlined,
              color: AppColors.primary,
            ),
            onPressed: () {
              setState(() {
                _isPasswordVisible = !_isPasswordVisible;
              });
            },
          ),
        ),
        const SizedBox(height: 5),
        const Align(
          alignment: Alignment.bottomRight,
          child: Text(
            'Forgot Password?',
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w500,
              color: AppColors.primary,
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildLoginButton() {
    return CustomButton(onTap: () async {
      final phone = _numController.text.trim(); // Assuming you use this for email now
      final password = _pwdController.text.trim();

      if (phone.isEmpty || password.isEmpty) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Please enter email and password')),
        );
        return;
      }

      final apiService = ApiService();
      final response = await apiService.login(phone: phone,password:  password);

      if (response != null && mounted) {
        String token = response['access'];
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('auth_token', token);
        print("Token saved!");
        print("Login successful! Token: ${response['access']}");
        Navigator.pushReplacementNamed(context, '/home');

      } else if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Login failed. Check credentials.')),
        );
      }
    }, text: 'Log In');
  }

  Widget _buildBottomSection() {
    return Center(
      child: Text.rich(
        TextSpan(
          text: 'New to Clickpic?? ',
          style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w500),
          children: <TextSpan>[
            TextSpan(
              recognizer: TapGestureRecognizer()
                ..onTap = () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => const SignupScreen(),
                    ),
                  );
                },
              text: 'Create Account ',
              style: const TextStyle(
                color: AppColors.primary,
                fontWeight: FontWeight.w600,
              ),
            ),
            const TextSpan(text: 'to Continue'),
          ],
        ),
      ),
    );
  }

  Widget _buildLabel(String text) {
    return Text(
      text,
      style: const TextStyle(
        fontSize: 16,
        fontWeight: FontWeight.w500,
        color: AppColors.primary,
      ),
    );
  }

  @override
  void dispose() {
    _numController.dispose();
    _pwdController.dispose();
    super.dispose();
  }
}
