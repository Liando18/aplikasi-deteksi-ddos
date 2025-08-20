import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:mobile_app/theme/app_pallete.dart';

class HeroWidgets extends StatelessWidget {
  const HeroWidgets({super.key});

  @override
  Widget build(BuildContext context) {
    return Stack(children: [content()]);
  }

  Container content() {
    return Container(
      padding: EdgeInsets.only(left: 16, right: 16, bottom: 16, top: 76),
      color: AppPallete.primary,
      child: Column(
        children: [
          Row(
            children: [
              Container(
                width: 50,
                height: 50,
                decoration: BoxDecoration(
                  image: const DecorationImage(
                    image: AssetImage("assets/imgs/user.png"),
                  ),
                  borderRadius: BorderRadius.circular(50),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
