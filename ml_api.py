import pickle
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# --- PATH CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "trained_diabet_model.sav"
SCALER_PATH = BASE_DIR / "trained_diabet_scalar.sav"
PUBLIC_DIR = BASE_DIR / "public"

app = FastAPI(title="Diabetes Predictor API")

# --- MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA SCHEMA ---
class InputData(BaseModel):
    pregnancies: int
    Glucose: int
    BloodPressure: int
    SkinThickness: int
    Insulin: int
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int

# --- LOAD ML MODELS ---
trained_diabetes_model = pickle.load(open(MODEL_PATH, "rb"))
trained_standard_scaler = pickle.load(open(SCALER_PATH, "rb"))

# --- SERVE FRONTEND (STANDALONE APP SETUP) ---
# Mount the public directory so the browser can load style.css and app.js
app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")

# Serve the main HTML file when someone visits the base URL
@app.get("/")
async def serve_home():
    return FileResponse(PUBLIC_DIR / "index.html")

# --- API ENDPOINTS ---
@app.get("/health")
async def health():
    return {"status": "ok", "message": "API is running natively!"}

@app.post("/diabetes_predict")
async def diabetes_predict(data: InputData):
    payload = data.model_dump()
    features = [
        payload["pregnancies"],
        payload["Glucose"],
        payload["BloodPressure"],
        payload["SkinThickness"],
        payload["Insulin"],
        payload["BMI"],
        payload["DiabetesPedigreeFunction"],
        payload["Age"],
    ]

    # Scale data and predict
    scaled_input_data = trained_standard_scaler.transform([features])
    prediction = trained_diabetes_model.predict(scaled_input_data)

    if prediction[0] == 1:
        return {"prediction": "The person is likely to have diabetes."}
    return {"prediction": "The person is unlikely to have diabetes."}
