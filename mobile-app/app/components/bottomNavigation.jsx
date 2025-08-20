import Ionicons from "@expo/vector-icons/Ionicons";
import { useRouter } from "expo-router";
import { useState } from "react";
import { StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export default function BottomNavigation() {
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const [activeTab, setActiveTab] = useState("Beranda");

  const navItems = [
    { icon: "home", label: "Beranda", route: "/" },
    { icon: "notifications", label: "Histori", route: "/histori" },
    { icon: "search", label: "Detection", route: "/detection" },
    { icon: "settings", label: "Pengaturan", route: "/pengaturan" },
    { icon: "person", label: "Akun", route: "/akun" },
  ];

  return (
    <View style={[styles.bottomNav, { marginBottom: insets.bottom || 8 }]}>
      {navItems.map((item) => (
        <TouchableOpacity
          key={item.label}
          style={styles.navItem}
          onPress={() => {
            setActiveTab(item.label);
            router.push(item.route);
          }}>
          <Ionicons
            name={item.icon}
            size={24}
            color={activeTab === item.label ? "#2e7d32" : "#2c2c2c"}
          />
          <Text
            style={[
              styles.navLabel,
              { color: activeTab === item.label ? "#2e7d32" : "#2c2c2c" },
            ]}>
            {item.label}
          </Text>
        </TouchableOpacity>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  bottomNav: {
    flexDirection: "row",
    backgroundColor: "#fff",
    borderRadius: 30,
    paddingVertical: 10,
    paddingHorizontal: 20,
    justifyContent: "space-between",
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 5,
    width: "95%",
    alignSelf: "center",
    position: "absolute",
    bottom: 0,
  },
  navItem: {
    alignItems: "center",
    justifyContent: "center",
  },
  navLabel: {
    fontSize: 12,
    marginTop: 2,
  },
});
