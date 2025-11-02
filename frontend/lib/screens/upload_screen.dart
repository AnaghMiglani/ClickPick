import 'dart:io';
import 'package:clickpic/screens/Details_screen.dart';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';

// --- FIXED IMPORTS ---
// Use package imports (package:...) instead of relative imports (../)
// Make sure your file names match (e.g., document_list_screen.dart)

import 'package:clickpic/constants/colors.dart';
import 'package:clickpic/widgets/custom_button.dart';
import 'package:clickpic/widgets/progressstepper.dart';
import 'package:clickpic/widgets/upload_box.dart';
import 'package:clickpic/screens/Details_screen.dart';

import '../widgets/cart_provider.dart'; // Correct navigation

// Note: I renamed the class to 'UploadScreen' from your original
// so it's consistent.
class UploadScreen extends StatelessWidget {
  const UploadScreen({super.key});

  /// This function opens the device's file explorer to pick files.
  void _pickFiles(BuildContext context) async {
    final cart = context.read<CartProvider>();
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        allowMultiple: true,
        type: FileType.custom,
        allowedExtensions: ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'],
      );

      if (result != null) {
        for (var platformFile in result.files) {
          if (platformFile.path != null) {
            cart.addFile(File(platformFile.path!));
          }
        }
      } else {
        print("User canceled file picking.");
      }
    } catch (e) {
      print("File picking error: $e");
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Failed to pick files. Check permissions.')),
      );
    }
  }

  /// This new function opens the camera to take a picture.
  void _pickFromCamera(BuildContext context) async {
    final cart = context.read<CartProvider>();
    final ImagePicker picker = ImagePicker();

    try {
      final XFile? image = await picker.pickImage(
        source: ImageSource.camera,
        imageQuality: 80,
      );

      if (image != null) {
        cart.addFile(File(image.path));
      } else {
        print("User canceled camera.");
      }
    } catch (e) {
      print("Camera error: $e");
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Failed to use camera. Check permissions.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    // Get the cart and listen for changes
    final cart = context.watch<CartProvider>();
    final cartItems = cart.itemList;

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text('Upload Document'),
        backgroundColor: Colors.white,
        elevation: 0,
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const ProgressStepper(currentStep: 0),
            const SizedBox(height: 32), // Increased spacing

            // "Browse files" box
            UploadBox(
              onTap: () => _pickFiles(context), // Correctly calls function
            ),
            const SizedBox(height: 16),

            // "Scan with Camera" button
            SizedBox(
              width: double.infinity,
              height: 50,
              child: OutlinedButton.icon(
                onPressed: () => _pickFromCamera(context),
                icon: const Icon(Icons.camera_alt_outlined, color: AppColors.primary),
                label: const Text(
                  'Scan with Camera',
                  style: TextStyle(
                      color: AppColors.primary, fontWeight: FontWeight.bold),
                ),
                style: OutlinedButton.styleFrom(
                  side: const BorderSide(color: AppColors.primary, width: 1.5),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12.0),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 24),

            const Text(
              'Uploaded Files',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),

            // --- RE-ADDED THE MISSING FILE LIST ---
            Expanded(
              child: cartItems.isEmpty
                  ? const Center(
                child: Text(
                  'No files uploaded yet.',
                  style: TextStyle(color: AppColors.gray),
                ),
              )
                  : ListView.builder(
                itemCount: cartItems.length,
                itemBuilder: (ctx, index) {
                  final item = cartItems[index];
                  return ListTile(
                    leading: const Icon(Icons.description_outlined,
                        color: AppColors.purple),
                    title: Text(
                      item.fileName,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(fontWeight: FontWeight.w500),
                    ),
                    trailing: IconButton(
                      icon: const Icon(Icons.delete_outline,
                          color: Colors.red),
                      onPressed: () {
                        context.read<CartProvider>().removeItem(item.id);
                      },
                    ),
                  );
                },
              ),
            ),
            const SizedBox(height: 16),

            CustomButton(
              text: 'Next',
              onTap: () {
                if (cartItems.isNotEmpty) {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (context) => const DetailsScreen()), // Navigate to the correct screen
                  );
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                        content: Text('Please upload at least one document.')),
                  );
                }
              },
            ),
          ],
        ),
      ),
    );
  }
}