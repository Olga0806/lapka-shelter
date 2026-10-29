import 'package:flutter/material.dart';
import '../api.dart';
import 'profile_screen.dart';

class ApplicationFormScreen extends StatefulWidget {
  final int animalId;
  final String animalName;

  const ApplicationFormScreen({
    super.key,
    required this.animalId,
    required this.animalName,
  });

  @override
  State<ApplicationFormScreen> createState() => _ApplicationFormScreenState();
}

class _ApplicationFormScreenState extends State<ApplicationFormScreen> {
  final _fullName = TextEditingController();
  final _phone = TextEditingController();
  final _age = TextEditingController(text: '18');
  final _familySize = TextEditingController(text: '1');
  final _otherAnimals = TextEditingController();
  final _comment = TextEditingController();
  String _housing = 'apartment';
  bool _loading = false;
  String? _error;

  Future<void> _submit() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      await Api.apply(
        animalId: widget.animalId,
        fullName: _fullName.text.trim(),
        phone: _phone.text.trim(),
        age: int.tryParse(_age.text) ?? 18,
        housing: _housing,
        familySize: int.tryParse(_familySize.text) ?? 1,
        otherAnimals: _otherAnimals.text.trim(),
        comment: _comment.text.trim(),
      );
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Заявка отправлена!')),
      );
      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (_) => const ProfileScreen()),
        (route) => false,
      );
    } catch (e) {
      setState(() {
        _error = e.toString().replaceFirst('Exception: ', '');
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Анкета усыновителя'),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Card(
              color: Colors.teal.shade50,
              child: ListTile(
                leading: const Icon(Icons.pets, color: Colors.teal),
                title: Text('Животное: ${widget.animalName}'),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _fullName,
              decoration: const InputDecoration(
                labelText: 'ФИО',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _phone,
              decoration: const InputDecoration(
                labelText: 'Телефон',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _age,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Возраст',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: _housing,
              decoration: const InputDecoration(
                labelText: 'Тип жилья',
                border: OutlineInputBorder(),
              ),
              items: const [
                DropdownMenuItem(value: 'apartment', child: Text('Квартира')),
                DropdownMenuItem(value: 'house', child: Text('Дом')),
              ],
              onChanged: (v) => setState(() => _housing = v ?? 'apartment'),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _familySize,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Человек в семье',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _otherAnimals,
              decoration: const InputDecoration(
                labelText: 'Другие животные (если есть)',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _comment,
              maxLines: 3,
              decoration: const InputDecoration(
                labelText: 'Комментарий',
                border: OutlineInputBorder(),
              ),
            ),
            if (_error != null) ...[
              const SizedBox(height: 12),
              Text(_error!, style: const TextStyle(color: Colors.red)),
            ],
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _loading ? null : _submit,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.teal,
                foregroundColor: Colors.white,
                minimumSize: const Size(double.infinity, 50),
              ),
              child: _loading
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text('Отправить заявку'),
            ),
          ],
        ),
      ),
    );
  }
}