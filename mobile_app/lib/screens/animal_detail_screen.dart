import 'package:flutter/material.dart';
import '../api.dart';
import 'login_screen.dart';
import 'application_form_screen.dart';

class AnimalDetailScreen extends StatefulWidget {
  final int id;
  const AnimalDetailScreen({super.key, required this.id});

  @override
  State<AnimalDetailScreen> createState() => _AnimalDetailScreenState();
}

class _AnimalDetailScreenState extends State<AnimalDetailScreen> {
  Map<String, dynamic>? _animal;
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final data = await Api.getAnimal(widget.id);
      setState(() {
        _animal = data;
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _loading = false;
      });
    }
  }

  Future<void> _apply() async {
    if (!await Api.isLoggedIn()) {
      if (!mounted) return;
      Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => const LoginScreen()),
      );
      return;
    }
    if (!mounted) return;
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => ApplicationFormScreen(
          animalId: widget.id,
          animalName: _animal?['name'] ?? '',
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_animal?['name'] ?? 'Животное'),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(child: Text('Ошибка: $_error'))
              : _buildBody(),
    );
  }

  Widget _buildBody() {
    final a = _animal!;
    final photos = a['photos'] as List<dynamic>? ?? [];

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        if (photos.isNotEmpty)
          SizedBox(
            height: 260,
            child: PageView.builder(
              itemCount: photos.length,
              itemBuilder: (_, i) => Padding(
                padding: const EdgeInsets.symmetric(horizontal: 4),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(12),
                  child: Image.network(
                    photos[i]['image'],
                    fit: BoxFit.cover,
                    errorBuilder: (_, __, ___) => Container(
                      color: Colors.grey[300],
                      child: const Icon(Icons.broken_image, size: 50),
                    ),
                  ),
                ),
              ),
            ),
          ),
        const SizedBox(height: 16),
        Text(a['name'] ?? '—',
            style: const TextStyle(fontSize: 26, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8,
          children: [
            Chip(label: Text(a['species_display'] ?? '')),
            Chip(label: Text(a['gender_display'] ?? '')),
            Chip(label: Text('${a['age']} лет')),
          ],
        ),
        const SizedBox(height: 16),
        _row('Порода', a['breed'] ?? '—'),
        _row('Описание', a['description'] ?? '—'),
        const SizedBox(height: 24),
        ElevatedButton.icon(
          onPressed: _apply,
          icon: const Icon(Icons.pets),
          label: const Text('Забрать животное'),
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.teal,
            foregroundColor: Colors.white,
            minimumSize: const Size(double.infinity, 50),
          ),
        ),
      ],
    );
  }

  Widget _row(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 100,
            child: Text(label,
                style: const TextStyle(fontWeight: FontWeight.bold)),
          ),
          Expanded(child: Text(value)),
        ],
      ),
    );
  }
}