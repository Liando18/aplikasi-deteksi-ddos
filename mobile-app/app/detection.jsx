import { useRef, useState } from "react";
import {
  Animated,
  Dimensions,
  Easing,
  ScrollView,
  StyleSheet,
  Text,
  TouchableWithoutFeedback,
  View,
} from "react-native";

const { width, height } = Dimensions.get("window");

const Detection = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [showTable, setShowTable] = useState(false);

  // Animations
  const scaleAnim = useRef(new Animated.Value(1)).current;
  const colorAnim = useRef(new Animated.Value(0)).current;
  const buttonPosition = useRef(new Animated.Value(height * 0.5 - 110)).current;
  const tableOpacity = useRef(new Animated.Value(0)).current;

  // Sample data
  const detectionData = [
    { date: "2023-05-15 08:30:45", status: "Detected" },
    { date: "2023-05-15 09:15:22", status: "Detected" },
    { date: "2023-05-15 10:42:10", status: "No Detection" },
    { date: "2023-05-15 11:05:33", status: "Detected" },
    { date: "2023-05-15 12:30:18", status: "No Detection" },
    { date: "2023-05-15 12:30:18", status: "No Detection" },
    { date: "2023-05-15 12:30:18", status: "No Detection" },
    { date: "2023-05-15 12:30:18", status: "No Detection" },
    { date: "2023-05-15 12:30:18", status: "No Detection" },
    { date: "2023-05-15 12:30:18", status: "No Detection" },
    { date: "2023-05-15 12:30:18", status: "No Detection" },
    { date: "2023-05-15 12:30:18", status: "No Detection" },
    { date: "2023-05-15 12:30:18", status: "No Detection" },
  ];

  const toggleDetection = () => {
    if (!isRunning) {
      // Start animation
      Animated.parallel([
        Animated.timing(buttonPosition, {
          toValue: height * 0.2 - 110, // Naik ke 30% dari layar
          duration: 400,
          easing: Easing.out(Easing.quad),
          useNativeDriver: false,
        }),
        Animated.timing(scaleAnim, {
          toValue: 0.8,
          duration: 400,
          easing: Easing.out(Easing.quad),
          useNativeDriver: true,
        }),
        Animated.timing(colorAnim, {
          toValue: 1,
          duration: 300,
          useNativeDriver: false,
        }),
        Animated.timing(tableOpacity, {
          toValue: 1,
          duration: 500,
          useNativeDriver: true,
        }),
      ]).start();

      setShowTable(true);
    } else {
      // Stop animation
      Animated.parallel([
        Animated.timing(buttonPosition, {
          toValue: height * 0.5 - 110,
          duration: 400,
          easing: Easing.out(Easing.quad),
          useNativeDriver: false,
        }),
        Animated.timing(scaleAnim, {
          toValue: 1,
          duration: 400,
          easing: Easing.out(Easing.quad),
          useNativeDriver: true,
        }),
        Animated.timing(colorAnim, {
          toValue: 0,
          duration: 300,
          useNativeDriver: false,
        }),
        Animated.timing(tableOpacity, {
          toValue: 0,
          duration: 300,
          useNativeDriver: true,
        }),
      ]).start(() => setShowTable(false));
    }

    setIsRunning(!isRunning);
  };

  const borderColor = colorAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ["#2e7d32", "#c62828"],
  });

  const textColor = borderColor;

  return (
    <View style={styles.container}>
      <Animated.View style={[styles.buttonContainer, { top: buttonPosition }]}>
        <TouchableWithoutFeedback onPress={toggleDetection}>
          <Animated.View style={{ transform: [{ scale: scaleAnim }] }}>
            <Animated.View
              style={[
                styles.button,
                {
                  borderColor,
                  borderWidth: 6,
                  backgroundColor: "transparent",
                },
              ]}>
              <Animated.Text style={[styles.buttonText, { color: textColor }]}>
                {isRunning ? "Stop" : "Start"}
              </Animated.Text>
            </Animated.View>
          </Animated.View>
        </TouchableWithoutFeedback>
      </Animated.View>

      {showTable && (
        <Animated.View
          style={[
            styles.tableContainer,
            {
              opacity: tableOpacity,
              top: height * 0.18 + 120,
            },
          ]}>
          <View style={styles.tableHeader}>
            <Text style={[styles.headerText, styles.dateColumn]}>Tanggal</Text>
            <Text style={[styles.headerText, styles.statusColumn]}>Status</Text>
          </View>

          <ScrollView
            style={styles.tableBody}
            showsVerticalScrollIndicator={false}>
            {detectionData.map((item, index) => (
              <View key={index} style={styles.tableRow}>
                <Text style={[styles.cellText, styles.dateColumn]}>
                  {item.date}
                </Text>
                <Text
                  style={[
                    styles.cellText,
                    styles.statusColumn,
                    {
                      color: item.status === "Detected" ? "#c62828" : "#2e7d32",
                      fontWeight: "bold",
                    },
                  ]}>
                  {item.status}
                </Text>
              </View>
            ))}
          </ScrollView>
        </Animated.View>
      )}
    </View>
  );
};

export default Detection;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f8f9fa",
  },
  buttonContainer: {
    position: "absolute",
    alignSelf: "center",
  },
  button: {
    width: 200,
    height: 200,
    borderRadius: 100,
    justifyContent: "center",
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 0,
  },
  buttonText: {
    fontSize: 26,
    fontWeight: "bold",
  },
  tableContainer: {
    position: "absolute",
    width: width * 0.9,
    alignSelf: "center",
    backgroundColor: "white",
    borderRadius: 12,
    padding: 15,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    maxHeight: height * 0.55,
  },
  tableHeader: {
    flexDirection: "row",
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#e0e0e0",
  },
  tableBody: {
    marginTop: 5,
  },
  tableRow: {
    flexDirection: "row",
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#f0f0f0",
  },
  headerText: {
    fontWeight: "bold",
    fontSize: 16,
    color: "#333",
  },
  cellText: {
    fontSize: 14,
    color: "#555",
  },
  dateColumn: {
    flex: 2,
    textAlign: "left",
    paddingLeft: 10,
  },
  statusColumn: {
    flex: 1,
    textAlign: "center",
  },
});
