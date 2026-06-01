# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pickle
import os

# Paths (relative to project root)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "model.pkl")
VECT_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "vectorizer.pkl")

# Load model & vectorizer once at startup
model = None
vectorizer = None
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VECT_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    print("Model and vectorizer loaded.")
except Exception as e:
    print("Warning: could not load model/vectorizer:", e)

app = FastAPI(title="Fake News Detector API")

# Allow CORS for development (tighten for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    prediction: str
    fake_probability: float
    real_probability: float

@app.get("/")
def root():
    return {"status": "ok", "info": "Fake News Detector API"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    global model, vectorizer
    if model is None or vectorizer is None:
        raise HTTPException(status_code=500, detail="Model or vectorizer not loaded on server.")
    text = req.text
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="No text provided for prediction.")
    x = vectorizer.transform([text])
    pred = model.predict(x)[0]
    # If model does not support predict_proba, this will error — but your logistic model should support it
    proba = model.predict_proba(x)[0]
    # Assuming 0 -> Fake, 1 -> Real (match your training encoding)
    fake_prob = float(proba[0])
    real_prob = float(proba[1])
    label = "Real" if pred == 1 else "Fake"
    return PredictResponse(prediction=label, fake_probability=fake_prob, real_probability=real_prob)

# Run with:
# uvicorn backend.main:app --host 0.0.0.0 --port 8000
