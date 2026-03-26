const form = document.getElementById("predict-form");
const sampleBtn = document.getElementById("sampleBtn");
const resultCard = document.getElementById("resultCard");
const resultText = document.getElementById("resultText");

const intFields = [
  "pregnancies",
  "Glucose",
  "BloodPressure",
  "SkinThickness",
  "Insulin",
  "Age",
];
const floatFields = ["BMI", "DiabetesPedigreeFunction"];

const samplePayload = {
  pregnancies: 2,
  Glucose: 120,
  BloodPressure: 70,
  SkinThickness: 20,
  Insulin: 85,
  BMI: 30.5,
  DiabetesPedigreeFunction: 0.5,
  Age: 45,
};

sampleBtn.addEventListener("click", () => {
  for (const [key, value] of Object.entries(samplePayload)) {
    const input = document.getElementById(key);
    if (input) input.value = value;
  }
  setResult("Sample values loaded. Click Predict.", "success");
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {};

  for (const key of intFields) {
    const value = Number.parseInt(form.elements[key].value, 10);
    if (!Number.isFinite(value)) {
      setResult(`Please enter a valid number for ${key}.`, "error");
      return;
    }
    payload[key] = value;
  }

  for (const key of floatFields) {
    const value = Number.parseFloat(form.elements[key].value);
    if (!Number.isFinite(value)) {
      setResult(`Please enter a valid number for ${key}.`, "error");
      return;
    }
    payload[key] = value;
  }

  // UPDATED: Now it just hits the same server directly!
  const endpoint = "/diabetes_predict";

  setResult("Predicting...", "success");

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const responseData = await response.json();
    if (!response.ok) {
      const detail = responseData.detail || "Request failed.";
      setResult(`API error: ${detail}`, "error");
      return;
    }

    setResult(responseData.prediction || "Prediction completed.", "success");
  } catch (error) {
    setResult(`Network error: ${error.message}`, "error");
  }
});

function setResult(message, state) {
  resultText.textContent = message;
  resultCard.classList.remove("success", "error");
  resultCard.classList.add(state);
}
