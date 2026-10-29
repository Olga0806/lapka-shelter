import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

// Адрес сервера Django. 
// Для работы по Wi-Fi используется IP твоего компьютера.
const String baseUrl = 'http://192.168.43.48:8000';

class Api {
  // ---------- Токен ----------
  static Future<void> saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('access_token', token);
  }

  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('access_token');
  }

  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token');
  }

  static Future<bool> isLoggedIn() async {
    final t = await getToken();
    return t != null && t.isNotEmpty;
  }

  // ---------- Животные ----------
  static Future<List<dynamic>> getAnimals({String? q, String? species}) async {
    final params = <String, String>{};
    if (q != null && q.isNotEmpty) params['q'] = q;
    if (species != null && species.isNotEmpty) params['species'] = species;

    final uri = Uri.parse('$baseUrl/api/animals/').replace(
      queryParameters: params.isEmpty ? null : params,
    );
    final resp = await http.get(uri);
    if (resp.statusCode == 200) {
      return jsonDecode(utf8.decode(resp.bodyBytes)) as List<dynamic>;
    }
    throw Exception('Ошибка загрузки: ${resp.statusCode}');
  }

  static Future<Map<String, dynamic>> getAnimal(int id) async {
    final resp = await http.get(Uri.parse('$baseUrl/api/animals/$id/'));
    if (resp.statusCode == 200) {
      return jsonDecode(utf8.decode(resp.bodyBytes)) as Map<String, dynamic>;
    }
    throw Exception('Ошибка загрузки: ${resp.statusCode}');
  }

  // ---------- Авторизация ----------
  static Future<void> login(String username, String password) async {
    final resp = await http.post(
      Uri.parse('$baseUrl/api/token/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'password': password}),
    );
    if (resp.statusCode == 200) {
      final data = jsonDecode(utf8.decode(resp.bodyBytes));
      await saveToken(data['access']);
    } else {
      throw Exception('Неверный логин или пароль');
    }
  }

  static Future<void> register({
    required String username,
    required String fullName,
    required String phone,
    required String password,
  }) async {
    final resp = await http.post(
      Uri.parse('$baseUrl/api/register/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'full_name': fullName,
        'phone': phone,
        'password': password,
      }),
    );
    if (resp.statusCode != 201) {
      final err = jsonDecode(utf8.decode(resp.bodyBytes));
      throw Exception('Ошибка регистрации: $err');
    }
  }

  // ---------- Профиль ----------
  static Future<Map<String, dynamic>> getProfile() async {
    final token = await getToken();
    final resp = await http.get(
      Uri.parse('$baseUrl/api/profile/'),
      headers: {'Authorization': 'Bearer $token'},
    );
    if (resp.statusCode == 200) {
      return jsonDecode(utf8.decode(resp.bodyBytes)) as Map<String, dynamic>;
    }
    throw Exception('Ошибка загрузки профиля: ${resp.statusCode}');
  }

  // ---------- Заявка ----------
  static Future<void> apply({
    required int animalId,
    required String fullName,
    required String phone,
    required int age,
    required String housing,
    required int familySize,
    required String otherAnimals,
    required String comment,
  }) async {
    final token = await getToken();
    final resp = await http.post(
      Uri.parse('$baseUrl/api/animals/$animalId/apply/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'full_name': fullName,
        'phone': phone,
        'age': age,
        'housing': housing,
        'family_size': familySize,
        'other_animals': otherAnimals,
        'comment': comment,
      }),
    );
    if (resp.statusCode != 201) {
      final err = jsonDecode(utf8.decode(resp.bodyBytes));
      throw Exception('Ошибка: $err');
    }
  }
}