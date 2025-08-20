import 'package:flutter/material.dart';
import 'package:mobile_app/theme/app_pallete.dart';
import 'package:mobile_app/widgets/hero_widgets.dart';

class DiscoverPage extends StatelessWidget {
  const DiscoverPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      bottomNavigationBar: bottomNavigationBar(),
      body: const SingleChildScrollView(
        child: Column(children: [HeroWidgets()]),
      ),
    );
  }

  BottomNavigationBar bottomNavigationBar() {
    return BottomNavigationBar(
      type: BottomNavigationBarType.fixed,
      backgroundColor: AppPallete.white,
      selectedItemColor: AppPallete.primary,
      unselectedItemColor: AppPallete.gray,
      showUnselectedLabels: true,
      items: [
        BottomNavigationBarItem(icon: Icon(Icons.home), label: "Home"),
        BottomNavigationBarItem(icon: Icon(Icons.play_arrow), label: "Deteksi"),
        BottomNavigationBarItem(icon: Icon(Icons.account_box), label: "Akun"),
      ],
    );
  }
}
