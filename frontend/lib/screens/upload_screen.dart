import 'dart:io';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import 'package:clickpic/constants/colors.dart';
import 'package:clickpic/widgets/custom_button.dart';
import 'package:clickpic/widgets/progressstepper.dart';
import 'package:clickpic/widgets/upload_box.dart';
import 'package:clickpic/screens/Details_screen.dart';
import 'package:clickpic/widgets/cart_provider.dart';

class UploadScreen extends StatelessWidget {
  const UploadScreen({super.key});

  void _pickFiles(BuildContext context) async {
    final cart = Provider.of<CartProvider>(context, listen: false);
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
      }
    } catch (e) {
      debugPrint("File picking error: $e");
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to pick files. Check permissions.')),
        );
      }
    }
  }

  void _pickFromCamera(BuildContext context) async {
    final cart = Provider.of<CartProvider>(context, listen: false);
    final ImagePicker picker = ImagePicker();

    try {
      final XFile? image = await picker.pickImage(
        source: ImageSource.camera,
        imageQuality: 80,
      );

      if (image != null) {
        cart.addFile(File(image.path));
      }
    } catch (e) {
      debugPrint("Camera error: $e");
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to use camera. Check permissions.')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text('Upload Document', style: TextStyle(color: Colors.black)),
        backgroundColor: Colors.white,
        elevation: 0,
        centerTitle: true,
      ),
      body: Consumer<CartProvider>(
        builder: (context, cart, child) {
          final cartItems = cart.itemList;

          return Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const ProgressStepper(currentStep: 0),
                const SizedBox(height: 32),

                UploadBox(
                  onTap: () => _pickFiles(context),
                ),
                const SizedBox(height: 16),

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

                Expanded(
                  child: cartItems.isEmpty
                      ? const Center(
                    child: Text(
                      'No files uploaded yet.',
                      style: TextStyle(color: AppColors.gray),
                    ),
                  )
                      : ListView.separated(
                    itemCount: cartItems.length,
                    separatorBuilder: (context, index) => const SizedBox(height: 8),
                    itemBuilder: (ctx, index) {
                      final item = cartItems[index];
                      return Container(
                        decoration: BoxDecoration(
                          color: Colors.grey[50],
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: Colors.grey[200]!),
                        ),
                        child: ListTile(
                          leading: Container(
                            padding: const EdgeInsets.all(8),
                            decoration: BoxDecoration(
                              color: AppColors.purple.withOpacity(0.1),
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: const Icon(Icons.description_outlined, color: AppColors.purple),
                          ),
                          title: Text(
                            item.fileName,
                            overflow: TextOverflow.ellipsis,
                            style: const TextStyle(fontWeight: FontWeight.w500),
                          ),
                          trailing: IconButton(
                            icon: const Icon(Icons.delete_outline, color: Colors.red),
                            onPressed: () {
                              // Using listen: false here as we are just calling a method, not rebuilding this specific widget
                              Provider.of<CartProvider>(context, listen: false).removeItem(item.id);
                            },
                          ),
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
                      Navigator.pushNamed(context, '/details');
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Please upload at least one document.')),
                      );
                    }
                  },
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}