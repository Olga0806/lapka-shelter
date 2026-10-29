import 'package:flutter/material.dart';
import 'screens/animal_list_screen.dart';

void main() {
  runApp(const ShelterApp());
}

class ShelterApp extends StatelessWidget {
  const ShelterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Лапка',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const AnimalListScreen(),
    );
  }
}