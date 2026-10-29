import 'package:flutter/material.dart';
import '../api.dart';
import 'animal_detail_screen.dart';
import 'login_screen.dart';
import 'profile_screen.dart';

class AnimalListScreen extends StatefulWidget {
  const AnimalListScreen({super.key});

  @override
  State<AnimalListScreen> createState() => _AnimalListScreenState();
}

class _AnimalListScreenState extends State<AnimalListScreen> {
  List<dynamic> _animals = [];
  bool _loading = true;
  String? _error;
  String _query = '';
  String _species = '';

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final data = await Api.getAnimals(q: _query, species: _species);
      setState(() {
        _animals = data;
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _loading = false;
      });
    }
  }

  Future<void> _openProfile() async {
    if (await Api.isLoggedIn()) {
      if (!mounted) return;
      Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => const ProfileScreen()),
      );
    } else {
      if (!mounted) return;
      Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => const LoginScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🐾 Лапка'),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.person),
            tooltip: 'Профиль',
            onPressed: _openProfile,
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(12),
            child: Column(
              children: [
                TextField(
                  decoration: const InputDecoration(
                    labelText: 'Поиск по кличке',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.search),
                  ),
                  onSubmitted: (v) {
                    _query = v;
                    _load();
                  },
                ),
                const SizedBox(height: 8),
                Row(
                  children: [
                    Expanded(
                      child: DropdownButtonFormField<String>(
                        value: _species.isEmpty ? null : _species,
                        decoration: const InputDecoration(
                          labelText: 'Вид',
                          border: OutlineInputBorder(),
                        ),
                        items: const [
                          DropdownMenuItem(value: '', child: Text('Все')),
                          DropdownMenuItem(value: 'dog', child: Text('Собаки')),
                          DropdownMenuItem(value: 'cat', child: Text('Кошки')),
                          DropdownMenuItem(value: 'other', child: Text('Другие')),
                        ],
                        onChanged: (v) {
                          _species = v ?? '';
                          _load();
                        },
                      ),
                    ),
                    const SizedBox(width: 8),
                    ElevatedButton(
                      onPressed: _load,
                      child: const Text('Найти'),
                    ),
                  ],
                ),
              ],
            ),
          ),
          Expanded(child: _buildList()),
        ],
      ),
    );
  }

  Widget _buildList() {
    if (_loading) return const Center(child: CircularProgressIndicator());
    if (_error != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error, color: Colors.red, size: 50),
              const SizedBox(height: 12),
              Text('Ошибка: $_error', textAlign: TextAlign.center),
              const SizedBox(height: 12),
              ElevatedButton(onPressed: _load, child: const Text('Повторить')),
            ],
          ),
        ),
      );
    }
    if (_animals.isEmpty) {
      return const Center(child: Text('Животных пока нет'));
    }
    return ListView.builder(
      itemCount: _animals.length,
      itemBuilder: (context, i) {
        final a = _animals[i];
        final photos = a['photos'] as List<dynamic>? ?? [];
        final imgUrl = photos.isNotEmpty ? photos[0]['image'] as String : null;

        return Card(
          margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          child: ListTile(
            leading: imgUrl != null
                ? ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.network(
                      imgUrl,
                      width: 60,
                      height: 60,
                      fit: BoxFit.cover,
                      errorBuilder: (_, __, ___) => Container(
                        width: 60,
                        height: 60,
                        color: Colors.grey[300],
                        child: const Icon(Icons.pets),
                      ),
                    ),
                  )
                : Container(
                    width: 60,
                    height: 60,
                    color: Colors.grey[300],
                    child: const Icon(Icons.pets),
                  ),
            title: Text(a['name'] ?? '—'),
            subtitle: Text(
              '${a['species_display']} • ${a['breed'] ?? '—'} • ${a['age']} лет',
            ),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => AnimalDetailScreen(id: a['id']),
                ),
              );
            },
          ),
        );
      },
    );
  }
}