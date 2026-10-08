# CropCompass 🌱

### Machine Learning-Based Crop Decision-Support System

CropCompass is a machine learning application that recommends crop categories based on soil and environmental conditions.

### 📊 Dataset
- 2,200 records
- 7 input features
- 22 crop classes
- 80:20 train-test split
- 1,760 training records and 440 testing records

### 🤖 Machine Learning
Two classification models were trained and compared:
- Logistic Regression — 97.27% accuracy
- Random Forest — 99.55% accuracy

Random Forest was selected as the final model.

### 🚀 Features
- Crop prediction
- Top-3 recommendations
- Model Agreement Analysis
- SHAP-based explainability
- What-If Analysis
- Prediction Reliability Analysis
- Model Performance dashboard
- Dataset & EDA
- SQLite prediction history

### 🛠️ Tech Stack
Python | Pandas | NumPy | Scikit-learn | SHAP | Streamlit | SQLite | Joblib

### 🌐 Live Demo
https://cropcompass.streamlit.app/


> CropCompass is a decision-support system based on patterns learned from historical data and is not a guarantee of agricultural success.
