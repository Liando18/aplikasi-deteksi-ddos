import { StyleSheet, Text, View } from "react-native";

export default function HomePage() {
  return (
    <View style={styles.container}>
      {/* Banner */}
      <View style={styles.banner}>
        <Text style={styles.bannerText}>Hallo, Aprilian</Text>
      </View>

      {/* Card */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Hesti Cantik</Text>
        <Text style={styles.cardBody}>
          Hesti sangatlah cantik imut dan baik, dia anak yang ceria, suka
          menolong sesama.
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f2f2f2",
  },
  banner: {
    backgroundColor: "seagreen",
    height: 250,
    padding: 16,
  },
  bannerText: {
    color: "#fff",
    fontSize: 24,
    fontWeight: "bold",
  },
  card: {
    position: "absolute",
    top: 70,
    left: 16,
    right: 16,
    backgroundColor: "#fff",
    borderRadius: 12,
    padding: 16,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 5,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 8,
  },
  cardBody: {
    fontSize: 14,
    color: "#555",
  },
});
