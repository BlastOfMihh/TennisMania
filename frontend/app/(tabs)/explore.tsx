import { ThemedText } from "@/components/ThemedText";
import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
} from "chart.js";
import { Line } from "react-chartjs-2";
import { ScrollView, StyleSheet, View } from "react-native";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default function TabTwoScreen() {
  const fakeAIData = {
    stats: {
      "Heart Rate Average": "132 BPM",
      "Projected Score with Break": "11-9",
      "Projected Score without Break": "9-11",
      Precision: "90%",
    },
    graphData: {
      heartRate: [120, 125, 130, 135, 140, 145, 148, 135, 125, 130, 138],
      scoreProjection: [8, 8, 9, 9, 10, 10, 11, 10, 9, 9, 11],
    },
    recommendation: "Take a break now for optimal performance!",
  };

  const chartData = {
    labels: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    datasets: [
      {
        label: "Heart Rate Over Time",
        data: fakeAIData.graphData.heartRate,
        borderColor: "blue",
        backgroundColor: "rgba(0, 0, 255, 0.2)",
        fill: true,
      },
      {
        label: "Score Projection",
        data: fakeAIData.graphData.scoreProjection,
        borderColor: "green",
        backgroundColor: "rgba(0, 255, 0, 0.2)",
        fill: true,
      },
    ],
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.recommendationContainer}>
        <ThemedText type="title" style={styles.recommendationText}>
          💡 Recommendation:
        </ThemedText>
        <ThemedText type="default" style={styles.recommendationText}>
          {fakeAIData.recommendation}
        </ThemedText>
      </View>

      <View style={styles.chartContainer}>
        <ThemedText type="subtitle" style={styles.chartTitle}>
          📈 Heart Rate and Score Projection
        </ThemedText>
        <Line data={chartData} />
      </View>

      <View style={styles.stats}>
        {Object.entries(fakeAIData.stats).map(([key, value]) => (
          <View style={styles.statRow} key={key}>
            <ThemedText type="subtitle" style={styles.statKey}>
              {key}:
            </ThemedText>
            <ThemedText type="default" style={styles.statValue}>
              {value}
            </ThemedText>
          </View>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  recommendationContainer: {
    alignItems: "center",
    marginTop: 50,
  },
  recommendationText: {
    color: "#FF0000",
    fontWeight: "bold",
    textAlign: "center",
    marginBottom: 10,
  },
  chartContainer: {
    marginTop: 40,
    alignItems: "center",
    justifyContent: "center",
    height: 300,
  },
  chartTitle: {
    marginBottom: 10,
    fontSize: 18,
    textAlign: "center",
  },
  stats: {
    marginTop: 20,
    alignItems: "center",
    marginBottom: 40,
  },
  statRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginVertical: 4,
  },
  statKey: {
    fontWeight: "bold",
    fontSize: 12,
  },
  statValue: {
    fontSize: 12,
  },
});
