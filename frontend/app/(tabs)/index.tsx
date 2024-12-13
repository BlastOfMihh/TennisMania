import { HelloWave } from "@/components/HelloWave";
import ParallaxScrollView from "@/components/ParallaxScrollView";
import { ThemedText } from "@/components/ThemedText";
import { ThemedView } from "@/components/ThemedView";
import { Ionicons } from "@expo/vector-icons";
import * as DocumentPicker from "expo-document-picker";
import * as FileSystem from "expo-file-system";
import { useRouter } from "expo-router";
import { useState } from "react";
import {
  Alert,
  Image,
  Platform,
  StyleSheet,
  TouchableOpacity,
  View,
} from "react-native";
export default function HomeScreen() {
  const [PolarCSVResult, setPolarCSVResult] = useState(null);
  const [ScoreCSVResult, setScoreCSVResult] = useState(null);
  const [CurrentTrainingSession, setCurrentTrainingSession] = useState(null);
  const router = useRouter();
  const processAndUploadFile = (fileContent: string, type: any) => {
    const rows = fileContent.split("\n").map((row) => row.split(","));

    const flattenedData = rows.map((row) => row.join(",")).join(",");

    console.log("Flattened Data:", flattenedData);

    uploadFile(flattenedData, type);
  };

  const handleFilePick = async (type: any) => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: "text/csv",
        copyToCacheDirectory: false,
      });

      if (result.canceled) {
        Alert.alert("file Selection Cancelled");
        return;
      }

      console.log("selected file:", result);
      const fileUri = result.assets[0].uri;

      if (Platform.OS === "web") {
        const file = result.assets[0].file;
        if (file) {
          const reader = new FileReader();

          reader.onload = (e) => {
            const fileContent = e.target?.result;

            processAndUploadFile(fileContent as string, type);

            //uploadFile(fileContent, type);
          };

          reader.onerror = (error) => {
            Alert.alert("error reading file");
          };

          reader.readAsText(new Blob([file], { type: "text/csv" }));
        } else {
          console.log("error in getting the file");
        }
      } else {
        const fileContent = await FileSystem.readAsStringAsync(fileUri);
        console.log("File content:", fileContent);
      }
    } catch (error) {
      console.error("Error picking file:", error);
      Alert.alert("Error", "An error occurred while picking the file.");
    }
  };

  const uploadFile = async (fileContent: any, type: any) => {
    var backendUrl = "http://10.220.22.21:5000/training_sessions";
    if (type == "PolarData")
      backendUrl = "http://10.220.22.21:5000/training_sessions";
    else {
      if (type == "ScoreData")
        backendUrl = "http://10.220.22.21:5000/training_sessions";
    }

    try {
      const payload = {
        content: fileContent,
      };

      const response = await fetch(backendUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("authToken")}`,
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        console.log("upload sucesssful");
        const responseData = await response.json();
        const trainingSessionId = responseData.id;
        console.log("Training Session ID:", trainingSessionId);
        setCurrentTrainingSession(trainingSessionId);
        if (trainingSessionId) {
          router.push("/explore");
        }
        return true;
      } else {
        console.error("upload failed:", await response.text());
        return false;
      }
    } catch (error) {
      console.error("error uploading file:", error);
      return false;
    }
  };

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: "#f6e48e", dark: "#1D3D47" }}
      headerImage={
        <View style={styles.headerContainer}>
          <Image
            source={require("@/assets/images/tennis3.png")}
            style={styles.headerImage}
          />
        </View>
      }
    >
      <ThemedView style={styles.titleContainer}>
        <ThemedText type="title">Welcome to TENNISMANIA!</ThemedText>
        <HelloWave />
      </ThemedView>
      <ThemedView style={styles.stepContainer}>
        <ThemedText style={styles.mediumText}>
          Please import your training data - CSV format
        </ThemedText>
        <View style={styles.buttonsContainer}>
          <TouchableOpacity
            style={styles.button}
            onPress={() => handleFilePick("PolarData")}
          >
            <Ionicons name="add-circle-outline" size={50} color="#d4d4d4" />
            <ThemedText style={styles.buttonText}>Polar Data</ThemedText>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.button}
            onPress={() => handleFilePick("ScoreData")}
          >
            <Ionicons name="add-circle-outline" size={50} color="#d4d4d4" />
            <ThemedText style={styles.buttonText}>Score Data</ThemedText>
          </TouchableOpacity>
        </View>
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  headerContainer: {
    flex: 1,
    backgroundColor: "#fff",
    justifyContent: "center",
    alignItems: "center",
    height: 100,
  },
  headerImage: {
    width: 300,
    height: 300,
    resizeMode: "contain",
  },
  titleContainer: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  stepContainer: {
    alignItems: "center",
    marginBottom: 8,
  },
  mediumText: {
    fontSize: 20,
    fontWeight: "bold",
    textAlign: "center",
    marginBottom: 16,
    color: "#d4d4d4",
  },
  buttonsContainer: {
    flexDirection: "row",
    justifyContent: "center",
    gap: 20,
    marginTop: 16,
  },
  button: {
    alignItems: "center",
    justifyContent: "center",
  },
  buttonText: {
    marginTop: 5,
    fontSize: 16,
    fontWeight: "bold",
    color: "#d4d4d4",
  },
});
