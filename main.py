from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("model.pkl")  # you need to export this from your notebook

class Record(BaseModel):
    record: dict

@app.post("/recommend")
def recommend(data: Record):
    df = pd.DataFrame([data.record])
    prediction = model.predict(df)[0]
    return {"price_recommended": round(float(prediction), 2)}

@app.post("/recommend_batch")
async def recommend_batch(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    predictions = model.predict(df)
    results = [{"price_recommended": round(float(p), 2)} for p in predictions]
    return {"recommendations": results, "kpis": {"total": len(results), "avg_price": round(float(sum(predictions)/len(predictions)), 2)}}
