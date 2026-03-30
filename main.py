from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import io
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("gradient_boosting_model.pkl")

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
    avg = round(float(sum(predictions) / len(predictions)), 2)
    return {"recommendations": results, "kpis": {"total_records": len(results), "avg_price": avg}}

@app.get("/")
def root():
    return {"status": "AI Price Optima API is running"}
```

---

### Step 3 — Update `requirements.txt`

Make sure it contains:
```
fastapi
uvicorn
joblib
scikit-learn
pandas
python-multipart
```

---

### Step 4 — Render start command

Make sure Render has:
```
uvicorn main:app --host 0.0.0.0 --port 8000
