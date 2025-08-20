import { ActivityIndicator, Text, View } from "react-native";

export default function SplashPage() {
  return (
    <View className="flex-1 items-center justify-center bg-blue-600">
      <ActivityIndicator size="large" color="white" />
      <Text className="text-white text-2xl mt-4">Loading...</Text>
    </View>
  );
}
