# PriceOptima – Dynamic Pricing Intelligence 🚀

PriceOptima is a **machine learning–based dynamic pricing system** that recommends optimal prices based on demand, supply, cost, and market conditions. The system helps businesses maximize revenue while maintaining customer satisfaction by making data-driven pricing decisions.

---

# 📌 Project Overview

Traditional pricing models rely on fixed rules or manual adjustments, which often fail to respond to changing market conditions. PriceOptima solves this problem by using **machine learning algorithms** to dynamically recommend prices.

The system analyzes multiple factors such as:

* Historical ride cost
* Number of riders (demand)
* Number of drivers (supply)
* Time of booking
* Customer loyalty status
* Location category
* Vehicle type

Based on these inputs, the model predicts the **optimal price that maximizes expected revenue while maintaining fairness and competitiveness.**

---

# 🎯 Key Features

✔ Dynamic price recommendation
✔ Machine learning based prediction
✔ Revenue optimization logic
✔ REST API using FastAPI
✔ Interactive React dashboard
✔ Batch price recommendations via CSV upload
✔ KPI analysis for revenue and conversion rates

---

# 🧠 Machine Learning Models Used

The project evaluates multiple regression models to determine the best pricing predictor:

* Random Forest Regressor
* Gradient Boosting Regressor
* XGBoost Regressor

Among these, **Gradient Boosting and XGBoost performed best** because they handle nonlinear relationships and complex feature interactions effectively.

---

# ⚙️ Technology Stack

## Frontend

* React.js
* Axios
* CSS

## Backend

* FastAPI
* Python

## Machine Learning

* Scikit-learn
* XGBoost
* Pandas
* NumPy

## Development Tools

* Google Colab (model development)
* VS Code (frontend)
* Git & GitHub

---

# 🏗️ Project Architecture

```
User Interface (React)
        │
        ▼
FastAPI Backend (REST API)
        │
        ▼
Feature Engineering Layer
        │
        ▼
Machine Learning Model
        │
        ▼
Price Optimization Logic
        │
        ▼
Recommendation Response
```

---

# 📊 System Workflow

1. User enters ride details in the React dashboard
2. Data is sent to the FastAPI backend
3. Feature engineering is applied
4. The machine learning model predicts completion probability
5. Price optimization algorithm selects the best price
6. Recommended price and KPIs are returned to the dashboard

---

# 📈 Output Example

The system returns:

* Recommended Price
* Completion Probability
* Revenue Prediction
* Price Bounds
* Gross Margin Percentage

Example:

```
{
  "price_recommended": 142.50,
  "p_complete_recommended": 0.84,
  "bounds": { "low": 130, "high": 150 },
  "gm_pct": 22.5
}
```

---

# 📂 Project Structure

```
PriceOptima
│
├── backend
│   ├── main.py
│   ├── dynamic_pricing.csv
│   └── pricing_model.joblib
│
├── frontend
│   ├── src
│   │   ├── App.js
│   │   ├── index.css
│   │   └── components
│
├── notebooks
│   └── model_training.ipynb
│
└── README.md
```

---

# ▶️ How to Run the Project

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/PriceOptima.git
cd PriceOptima
```

---

## 2️⃣ Run the FastAPI Backend

Install dependencies:

```bash
pip install fastapi uvicorn pandas numpy scikit-learn xgboost joblib
```

Run server:

```bash
uvicorn main:app --reload
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

## 3️⃣ Run the React Frontend

Navigate to frontend folder:

```bash
cd frontend
```

Install packages:

```bash
npm install
```

Start React app:

```bash
npm start
```

Frontend runs on:

```
http://localhost:3000
```

---

# 📊 Model Evaluation

The models were evaluated using **R² Score**.

Best model performance:

```
R² Score ≈ 0.87
```

This indicates strong predictive capability for pricing optimization.

---

# 🚀 Future Improvements

* Real-time competitor price integration
* Reinforcement learning based pricing
* Cloud deployment
* Explainable AI using SHAP
* Live dashboard analytics

---

# 👩‍💻 Author

**Deepika D**
Computer Science And Business System (CSBS)

---

# ⭐ Final Note

PriceOptima demonstrates how **machine learning, backend APIs, and modern frontend frameworks can be combined to build intelligent decision systems for real-world business problems.**

# ⭐ Deployment Link

https://ai-price-optima-iota.vercel.app/

