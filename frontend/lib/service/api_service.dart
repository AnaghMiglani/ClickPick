import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/order.dart';
import 'package:clickpic/models/print_jon.dart';


class ApiService {
  static const String baseUrl = 'http://192.168.0.157:8000';

  /// Calls your backend to create a Razorpay order.
  /// Returns the 'order_id' if successful, or null if it fails.
  Future<String?> createRazorpayOrder(double amountInRupees) async {
    return 'order_test_${DateTime.now().millisecondsSinceEpoch}';
    // try {
    //   final url = Uri.parse('$baseUrl/stationery/create-printout');
    //
    //   final amountInPaise = (amountInRupees * 100).toInt();
    //
    //   final response = await http.post(
    //     url,
    //     headers: {'Content-Type': 'application/json'},
    //     body: jsonEncode({
    //       'amount': amountInPaise,
    //       'currency': 'INR',
    //     }),
    //   );
    //
    //   if (response.statusCode == 200) {
    //     final data = jsonDecode(response.body);
    //     return data['order_id'];
    //   } else {
    //     print('Backend Error: ${response.body}');
    //     return null;
    //   }
    // } catch (e) {
    //   print('Network Error: $e');
    //   return null;
    // }
  }

  Future<double?> calculateTotalCost(List<PrintJob> jobs) async {
    try {
      final url = Uri.parse('$baseUrl/stationery/calculate-cost/');
      var request = http.MultipartRequest('POST', url);

      for (var job in jobs) {
        request.files.add(await http.MultipartFile.fromPath('files', job.file.path));
        if (job.color == 'Colored') {
          request.files.add(http.MultipartFile.fromString('colouredpages', 'ALL'));
          request.files.add(http.MultipartFile.fromString('pages', ''));
        } else {
          request.files.add(http.MultipartFile.fromString('colouredpages', ''));
          request.files.add(http.MultipartFile.fromString('pages', 'ALL'));
        }
      }

      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return double.tryParse(data['cost'].toString());
      } else {
        print("Cost calculation failed: ${response.body}");
        return null;
      }
    } catch (e) {
      print("Error calculating cost: $e");
      return null;
    }
  }
  Future<Map<String, dynamic>?> login({String? email, String? phone, required String password}) async {
    try {
      final url = Uri.parse('$baseUrl/auth/login/');

      final Map<String, dynamic> body = {'password': password};
      if (email != null && email.isNotEmpty) {
        body['email'] = email;
      } else if (phone != null && phone.isNotEmpty) {
        body['number'] = phone;
      }

      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print('Login failed: ${response.body}');
        return null;
      }
    } catch (e) {
      print('Error during login: $e');
      return null;
    }
  }
  Future<bool> uploadPrintOrders(List<PrintJob> jobs, double totalCost) async {
    try {
      final url = Uri.parse('$baseUrl/stationery/create-printout/');
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('auth_token');

      var request = http.MultipartRequest('POST', url);
      request.headers['Authorization'] = 'Bearer $token';

      String costPerFile = (totalCost / jobs.length).toStringAsFixed(2);

      for (var job in jobs) {
        request.files.add(await http.MultipartFile.fromPath('files', job.file.path));

        request.files.add(http.MultipartFile.fromString(
            'colouredpages', job.color == 'Colored' ? 'ALL' : ''));

        request.files.add(http.MultipartFile.fromString(
            'pages', job.color == 'Black & White' ? 'ALL' : ''));

        request.files.add(http.MultipartFile.fromString(
            'costs', costPerFile));

        request.files.add(http.MultipartFile.fromString(
            'custom_messages', job.comments));

        request.files.add(http.MultipartFile.fromString(
            'print_on_one_side_list', 'True')); // Default value
      }

      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 201 || response.statusCode == 200) {
        return true;
      } else {
        print("Upload failed: ${response.body}");
        return false;
      }
    } catch (e) {
      print("Error uploading: $e");
      return false;
    }
  }
  /// FETCH ACTIVE PRINTOUTS
  Future<List<dynamic>> fetchActivePrintouts() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('auth_token');

      final response = await http.get(
        Uri.parse('$baseUrl/stationery/active-printouts/'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to load active printouts: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching active printouts: $e');
      return [];
    }
  }

  Future<List<dynamic>> fetchPastPrintouts() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('auth_token');

      final response = await http.get(
        Uri.parse('$baseUrl/stationery/past-printouts/'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to load past printouts');
      }
    } catch (e) {
      print('Error fetching past printouts: $e');
      return [];
    }
  }
  Future<List<Order>> fetchPastOrders() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('auth_token');

      final response = await http.get(
        Uri.parse('$baseUrl/stationery/past-orders/'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Order.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load past orders');
      }
    } catch (e) {
      print('Error fetching past orders: $e');
      return [];
    }
  }
}