import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { StyleSheet } from "react-native";
import { SafeAreaProvider, SafeAreaView } from "react-native-safe-area-context";
import BottomNavigation from "./components/bottomNavigation";

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <StatusBar style="dark" translucent />
      <SafeAreaView style={styles.container} edges={["top", "bottom"]}>
        <Stack screenOptions={{ headerShown: false }} />
        <BottomNavigation />
      </SafeAreaView>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f2f2f2",
  },
});
