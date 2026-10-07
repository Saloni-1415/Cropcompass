import streamlit as st
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
 
 
# =========================================================
# PAGE CONFIGURATION
# =========================================================
 
st.set_page_config(
    page_title="CropCompass",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
 
# =========================================================
# CUSTOM CSS
# =========================================================
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
 
:root {
    --green-900: #0f2e1f;
    --green-800: #14402b;
    --green-700: #1a5538;
    --green-600: #1f6b43;
    --green-500: #2f8a5a;
    --green-100: #e3f1e8;
    --green-50:  #f1f8f3;
    --ink:       #16291e;
    --muted:     #647067;
    --line:      #e3e9e4;
    --canvas:    #f5f7f5;
    --white:     #ffffff;
}
 
html, body, [class*="css"], .stApp, button, input, select, textarea {
    font-family: 'Inter', -apple-system, 'Segoe UI', Roboto, sans-serif;
}
 
.stApp {
    background-color: var(--canvas);
}
 
.block-container {
    max-width: 1280px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}
 
/* Hide default Streamlit chrome */
#MainMenu, footer {
    visibility: hidden;
}
 
header[data-testid="stHeader"] {
    background: transparent;
}
 
h1, h2, h3 {
    color: var(--ink);
    letter-spacing: -0.02em;
}
 
 
/* ---------------------------------------------------------
   SIDEBAR
--------------------------------------------------------- */
 
[data-testid="stSidebar"] {
    background-color: var(--green-900);
    border-right: none;
}
 
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}
 
[data-testid="stSidebar"] * {
    color: #ffffff;
}
 
.sidebar-brand {
    padding: 4px 6px 22px 6px;
    margin-bottom: 20px;
    border-bottom: 1px solid rgba(255,255,255,0.12);
}
 
.sidebar-title {
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.4px;
}
 
.sidebar-subtitle {
    font-size: 12.5px;
    color: #a9c7b5 !important;
    margin-top: 6px;
    line-height: 1.5;
}
 
.sidebar-section {
    font-size: 11.5px;
    font-weight: 600;
    letter-spacing: 0.6px;
    color: #8fb29d !important;
    padding: 0 6px;
    margin-bottom: 8px;
}
 
/* Navigation as clean list items instead of radio buttons */
[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 2px;
}
 
[data-testid="stSidebar"] div[role="radiogroup"] > label {
    width: 100%;
    padding: 10px 12px;
    border-radius: 9px;
    margin: 0;
    cursor: pointer;
    transition: background-color 0.15s ease;
}
 
[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
    display: none;
}
 
[data-testid="stSidebar"] div[role="radiogroup"] > label p {
    font-size: 14.5px;
    font-weight: 500;
    color: #cfe2d6 !important;
}
 
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background-color: rgba(255,255,255,0.07);
}
 
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
    background-color: rgba(255,255,255,0.13);
}
 
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p {
    color: #ffffff !important;
    font-weight: 600;
}
 
 
/* ---------------------------------------------------------
   PAGE HEADER
--------------------------------------------------------- */
 
.page-title {
    color: var(--ink);
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -0.8px;
    line-height: 1.2;
    margin: 0;
}
 
.page-description {
    color: var(--muted);
    font-size: 15.5px;
    line-height: 1.6;
    margin-top: 8px;
    max-width: 680px;
}
 
.page-divider {
    height: 1px;
    background-color: var(--line);
    margin: 26px 0 30px 0;
}
 
 
/* ---------------------------------------------------------
   HERO
--------------------------------------------------------- */
 
.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #0f3524 0%, #1c6341 100%);
    border-radius: 20px;
    padding: 52px 52px 48px 52px;
    margin-bottom: 40px;
    color: white;
}
 
.hero::after {
    content: "";
    position: absolute;
    right: -90px;
    top: -90px;
    width: 340px;
    height: 340px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0) 70%);
}
 
.hero-label {
    font-size: 12.5px;
    font-weight: 500;
    letter-spacing: 0.4px;
    color: #a9d3b9;
    margin-bottom: 14px;
}
 
.hero-title {
    position: relative;
    font-size: 44px;
    font-weight: 700;
    line-height: 1.12;
    letter-spacing: -1.4px;
    margin: 0;
}
 
.hero-description {
    position: relative;
    max-width: 620px;
    margin-top: 18px;
    font-size: 16.5px;
    line-height: 1.7;
    color: #d7e9de;
}
 
.hero-status {
    position: relative;
    display: inline-block;
    margin-top: 26px;
    padding: 7px 14px;
    border-radius: 999px;
    background-color: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.18);
    font-size: 12.5px;
    font-weight: 500;
}
 
 
/* ---------------------------------------------------------
   SECTION HEADINGS
--------------------------------------------------------- */
 
.section-title {
    color: var(--ink);
    font-size: 20px;
    font-weight: 650;
    letter-spacing: -0.3px;
    margin-top: 6px;
    margin-bottom: 4px;
}
 
.section-subtitle {
    color: var(--muted);
    font-size: 14.5px;
    margin-bottom: 20px;
}
 
 
/* ---------------------------------------------------------
   METRIC CARDS
--------------------------------------------------------- */
 
[data-testid="stMetric"] {
    background-color: var(--white);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 20px 22px;
}
 
[data-testid="stMetricLabel"] p {
    color: var(--muted) !important;
    font-size: 13.5px;
    font-weight: 500;
}
 
[data-testid="stMetricValue"] {
    color: var(--green-800) !important;
    font-weight: 700;
    letter-spacing: -0.5px;
}
 
 
/* ---------------------------------------------------------
   MODEL CARDS
--------------------------------------------------------- */
 
.model-card {
    background-color: var(--white);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 26px 28px;
    min-height: 168px;
}
 
.model-card-selected {
    background-color: var(--green-50);
    border: 1.5px solid var(--green-500);
}
 
.model-name {
    color: var(--ink);
    font-size: 16px;
    font-weight: 600;
}
 
.model-accuracy {
    color: var(--green-600);
    font-size: 36px;
    font-weight: 700;
    letter-spacing: -1px;
    margin-top: 10px;
    line-height: 1.1;
}
 
.model-caption {
    color: var(--muted);
    font-size: 13px;
    margin-top: 4px;
}
 
.model-badge {
    display: inline-block;
    margin-top: 14px;
    padding: 5px 11px;
    border-radius: 999px;
    background-color: var(--green-100);
    color: var(--green-700);
    font-size: 12px;
    font-weight: 600;
}
 
 
/* ---------------------------------------------------------
   PROCESS CARDS
--------------------------------------------------------- */
 
.process-card {
    background-color: var(--white);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 26px 28px;
    min-height: 190px;
}
 
.process-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: var(--green-100);
    color: var(--green-700);
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 16px;
}
 
.process-title {
    color: var(--ink);
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 8px;
}
 
.process-text {
    color: var(--muted);
    font-size: 14.5px;
    line-height: 1.65;
}
 
 
/* ---------------------------------------------------------
   PREDICTION PAGE
--------------------------------------------------------- */
 
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--white);
    border-color: var(--line);
    border-radius: 14px;
}
 
.input-group-title {
    color: var(--ink);
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 4px;
}
 
.info-note {
    background-color: var(--green-50);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 14px 16px;
    margin-top: 14px;
    color: var(--muted);
    font-size: 13px;
    line-height: 1.6;
}
 
.info-note b {
    color: var(--green-800);
}
 
[data-testid="stWidgetLabel"] p {
    color: #33473a;
    font-size: 13.5px;
    font-weight: 500;
}
 
.result-box {
    background-color: var(--green-50);
    border: 1px solid #bcdcc8;
    border-radius: 14px;
    padding: 30px 24px;
    text-align: center;
}
 
.result-label {
    color: #5b7a67;
    font-size: 13.5px;
    font-weight: 500;
}
 
.result-crop {
    color: var(--green-700);
    font-size: 36px;
    font-weight: 700;
    letter-spacing: -0.8px;
    margin-top: 6px;
}
 
 
/* ---------------------------------------------------------
   BUTTONS
--------------------------------------------------------- */
 
.stButton > button {
    background-color: var(--green-600);
    color: white;
    border: none;
    border-radius: 10px;
    min-height: 48px;
    font-size: 15px;
    font-weight: 600;
    transition: background-color 0.15s ease;
}
 
.stButton > button:hover {
    background-color: var(--green-700);
    color: white;
    border: none;
}
 
.stButton > button:focus-visible {
    outline: 2px solid var(--green-500);
    outline-offset: 2px;
}
 
 
/* ---------------------------------------------------------
   INPUTS
--------------------------------------------------------- */
 
div[data-baseweb="input"],
div[data-baseweb="select"] {
    border-radius: 9px;
}
 
div[data-baseweb="input"]:focus-within {
    border-color: var(--green-500) !important;
}
 
 
/* ---------------------------------------------------------
   ALERTS
--------------------------------------------------------- */
 
[data-testid="stAlert"] {
    border-radius: 12px;
    border: 1px solid var(--line);
}
 
 
/* ---------------------------------------------------------
   GENERAL
--------------------------------------------------------- */
 
hr {
    border-color: var(--line);
}
 
[data-testid="stCaptionContainer"] {
    color: var(--muted);
}
 
</style>
""", unsafe_allow_html=True)
 
 
# =========================================================
# HELPERS
# =========================================================
 
def page_header(title, description):
    st.markdown(f"""
<div class="page-title">{title}</div>
<div class="page-description">{description}</div>
<div class="page-divider"></div>
""", unsafe_allow_html=True)
 
 
def section_header(title, subtitle=None):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )
 
    if subtitle:
        st.markdown(
            f'<div class="section-subtitle">{subtitle}</div>',
            unsafe_allow_html=True
        )
 
 
def spacer():
    st.markdown("<br>", unsafe_allow_html=True)
 
 
# =========================================================
# LOAD SAVED MODELS
# =========================================================
 
random_forest_model = joblib.load(
    "models/random_forest_model.pkl"
)
 
logistic_model = joblib.load(
    "models/logistic_model.pkl"
)
 
metadata = joblib.load(
    "models/cropcompass_metadata.pkl"
)
 
# StandardScaler used while training Logistic Regression.
# Logistic Regression needs scaled input; Random Forest does not.
try:
    scaler = joblib.load("models/scaler.pkl")
except FileNotFoundError:
    scaler = None
 
 
def prepare_input_for_logistic(data):
    """
    Scale the input before giving it to Logistic Regression.
 
    - If the saved model is already a Pipeline, scaling is built in,
      so the data is returned as it is.
    - If a separate scaler is available, apply it.
    - Otherwise return the data unchanged.
    """
    if isinstance(logistic_model, Pipeline):
        return data
 
    if scaler is not None:
        return pd.DataFrame(
            scaler.transform(data),
            columns=data.columns
        )
 
    return data
 
 
# =========================================================
# SIDEBAR
# =========================================================
 
st.sidebar.markdown("""
<div class="sidebar-brand">
<div class="sidebar-title">🌱 CropCompass</div>
<div class="sidebar-subtitle">Data-driven crop decision support</div>
</div>
<div class="sidebar-section">Navigation</div>
""", unsafe_allow_html=True)
 
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🌾 Crop Prediction",
        "📊 Model Performance",
        "🔍 Explainability",
        "🧪 What-If Analysis",
        "📜 Prediction History",
        "📈 Dataset & EDA",
        "👥 Team"
    ],
    label_visibility="collapsed"
)
 
 
# =========================================================
# DASHBOARD
# =========================================================
 
if page == "🏠 Dashboard":
 
    st.markdown("""
<div class="hero">
<div class="hero-label">Machine Learning • Smart Agriculture</div>
<div class="hero-title">Smarter crop decisions,<br>backed by data.</div>
<div class="hero-description">
CropCompass analyzes soil and environmental conditions using trained
machine learning models to provide data-driven crop recommendations.
</div>
<div class="hero-status">● Models ready for prediction</div>
</div>
""", unsafe_allow_html=True)
 
    section_header(
        "Project Overview",
        "A quick look at the dataset and machine learning system."
    )
 
    col1, col2, col3, col4 = st.columns(4)
 
    with col1:
        st.metric("Dataset Records", "2,200")
 
    with col2:
        st.metric("Crop Classes", "22")
 
    with col3:
        st.metric("Input Features", "7")
 
    with col4:
        st.metric("Best Accuracy", "99.55%")
 
    spacer()
 
 
    # -----------------------------------------------------
    # MODEL PERFORMANCE
    # -----------------------------------------------------
 
    section_header(
        "Model Performance",
        "Two classification algorithms were trained and compared."
    )
 
    col1, col2 = st.columns(2)
 
    with col1:
 
        st.markdown("""
<div class="model-card">
<div class="model-name">Logistic Regression</div>
<div class="model-accuracy">97.27%</div>
<div class="model-caption">Test Accuracy</div>
</div>
""", unsafe_allow_html=True)
 
    with col2:
 
        st.markdown("""
<div class="model-card model-card-selected">
<div class="model-name">Random Forest</div>
<div class="model-accuracy">99.55%</div>
<div class="model-caption">Test Accuracy</div>
<div class="model-badge">✓ Selected model</div>
</div>
""", unsafe_allow_html=True)
 
    spacer()
 
 
    # -----------------------------------------------------
    # HOW IT WORKS
    # -----------------------------------------------------
 
    section_header(
        "How CropCompass Works",
        "From input conditions to a machine learning prediction."
    )
 
    col1, col2, col3 = st.columns(3)
 
    with col1:
 
        st.markdown("""
<div class="process-card">
<div class="process-number">1</div>
<div class="process-title">Enter Conditions</div>
<div class="process-text">
Provide soil nutrient values and environmental conditions
such as temperature, humidity, pH and rainfall.
</div>
</div>
""", unsafe_allow_html=True)
 
    with col2:
 
        st.markdown("""
<div class="process-card">
<div class="process-number">2</div>
<div class="process-title">Run Prediction</div>
<div class="process-text">
The trained machine learning models analyze the seven
input features and identify the most suitable crop category.
</div>
</div>
""", unsafe_allow_html=True)
 
    with col3:
 
        st.markdown("""
<div class="process-card">
<div class="process-number">3</div>
<div class="process-title">Understand Results</div>
<div class="process-text">
View the recommended crop, alternative predictions and
agreement between the trained models.
</div>
</div>
""", unsafe_allow_html=True)
 
    spacer()
 
    st.caption(
        "CropCompass is a decision-support system based on historical "
        "dataset patterns and should not be treated as a guaranteed "
        "agricultural recommendation."
    )
 
 
# =========================================================
# CROP PREDICTION
# =========================================================
 
elif page == "🌾 Crop Prediction":
 
    page_header(
        "Crop Prediction",
        "Enter the soil and environmental conditions to generate "
        "a crop prediction."
    )
 
    section_header(
        "Soil & Environmental Conditions",
        "Use values within the range represented in the training dataset."
    )
 
    col1, col2, col3 = st.columns(3)
 
    with col1:
 
        with st.container(border=True):
 
            st.markdown(
                '<div class="input-group-title">Soil Nutrients</div>',
                unsafe_allow_html=True
            )
 
            nitrogen = st.number_input(
                "Nitrogen (N)",
                min_value=0.0,
                max_value=140.0,
                value=50.0
            )
 
            phosphorus = st.number_input(
                "Phosphorus (P)",
                min_value=5.0,
                max_value=145.0,
                value=50.0
            )
 
            potassium = st.number_input(
                "Potassium (K)",
                min_value=5.0,
                max_value=205.0,
                value=50.0
            )
 
    with col2:
 
        with st.container(border=True):
 
            st.markdown(
                '<div class="input-group-title">Climate</div>',
                unsafe_allow_html=True
            )
 
            temperature = st.number_input(
                "Temperature (°C)",
                min_value=8.0,
                max_value=44.0,
                value=25.0
            )
 
            humidity = st.number_input(
                "Humidity (%)",
                min_value=14.0,
                max_value=100.0,
                value=70.0
            )
 
    with col3:
 
        with st.container(border=True):
 
            st.markdown(
                '<div class="input-group-title">Soil & Water</div>',
                unsafe_allow_html=True
            )
 
            ph = st.number_input(
                "Soil pH",
                min_value=3.5,
                max_value=9.9,
                value=6.5
            )
 
            rainfall = st.number_input(
                "Rainfall (mm)",
                min_value=20.0,
                max_value=299.0,
                value=100.0
            )
 
    spacer()
 
    if st.button(
        "🌱 Predict Crop",
        use_container_width=True
    ):
 
        # Keep feature names identical to the training dataset
        input_data = pd.DataFrame([{
            "N": nitrogen,
            "P": phosphorus,
            "K": potassium,
            "temperature": temperature,
            "humidity": humidity,
            "ph": ph,
            "rainfall": rainfall
        }])
 
 
        # Logistic Regression needs scaled input (same scaling as training)
        logistic_input = prepare_input_for_logistic(input_data)
 
 
        # Predictions
        rf_prediction = random_forest_model.predict(
            input_data
        )[0]
 
        lr_prediction = logistic_model.predict(
            logistic_input
        )[0]
 
 
        # Random Forest probabilities
        rf_probabilities = random_forest_model.predict_proba(
            input_data
        )[0]
 
        class_names = random_forest_model.classes_
 
        sorted_indices = rf_probabilities.argsort()[::-1]
 
        top_3 = []
 
        for index in sorted_indices[:3]:
 
            top_3.append(
                (
                    class_names[index],
                    rf_probabilities[index] * 100
                )
            )
 
        st.divider()
 
 
        # -------------------------------------------------
        # MAIN RESULT
        # -------------------------------------------------
 
        section_header("Prediction Result")
 
        st.markdown(f"""
<div class="result-box">
<div class="result-label">Recommended Crop</div>
<div class="result-crop">{rf_prediction.title()}</div>
</div>
""", unsafe_allow_html=True)
 
        spacer()
 
 
        # -------------------------------------------------
        # TOP 3
        # -------------------------------------------------
 
        section_header("Top 3 Recommendations")
 
        col1, col2, col3 = st.columns(3)
 
        columns = [col1, col2, col3]
 
        for position, (crop, score), column in zip(
            range(1, 4),
            top_3,
            columns
        ):
 
            with column:
 
                st.metric(
                    f"#{position} {crop.title()}",
                    f"{score:.2f}%"
                )
 
        spacer()
 
 
        # -------------------------------------------------
        # MODEL AGREEMENT
        # -------------------------------------------------
 
        section_header("Model Agreement")
 
        col1, col2 = st.columns(2)
 
        with col1:
 
            st.info(
                f"Logistic Regression: "
                f"**{lr_prediction.title()}**"
            )
 
        with col2:
 
            st.success(
                f"Random Forest: "
                f"**{rf_prediction.title()}**"
            )
 
 
        if rf_prediction == lr_prediction:
 
            st.success(
                "✓ Both models agree on the recommended crop."
            )
 
        else:
 
            st.warning(
                "⚠ The two models produced different predictions."
            )
 
 
# =========================================================
# MODEL PERFORMANCE
# =========================================================
 
elif page == "📊 Model Performance":
 
    page_header(
        "Model Performance",
        "Comparison of the machine learning models trained for CropCompass."
    )
 
    col1, col2 = st.columns(2)
 
    with col1:
 
        st.markdown("""
<div class="model-card">
<div class="model-name">Logistic Regression</div>
<div class="model-accuracy">97.27%</div>
<div class="model-caption">Test accuracy</div>
</div>
""", unsafe_allow_html=True)
 
    with col2:
 
        st.markdown("""
<div class="model-card model-card-selected">
<div class="model-name">Random Forest</div>
<div class="model-accuracy">99.55%</div>
<div class="model-caption">Test accuracy</div>
<div class="model-badge">✓ Selected model</div>
</div>
""", unsafe_allow_html=True)
 
    spacer()
 
    st.info(
        "Random Forest was selected as the final model because it achieved "
        "the higher test accuracy."
    )
 
 
# =========================================================
# PREDICTION EXPLAINABILITY
# =========================================================
 
elif page == "🔍 Explainability":
 
    page_header(
        "Prediction Explainability",
        "Understand which input features contributed to the "
        "Random Forest prediction."
    )
 
    # -----------------------------------------------------
    # INPUTS
    # -----------------------------------------------------
 
    section_header(
        "Input Conditions",
        "Enter the same soil and environmental conditions used "
        "for a prediction."
    )
 
    col1, col2, col3 = st.columns(3)
 
    with col1:
 
        with st.container(border=True):
 
            st.markdown(
                '<div class="input-group-title">Soil Nutrients</div>',
                unsafe_allow_html=True
            )
 
            nitrogen = st.number_input(
                "Nitrogen (N)",
                min_value=0.0,
                max_value=140.0,
                value=50.0,
                step=0.1,
                key="shap_n"
            )
 
            phosphorus = st.number_input(
                "Phosphorus (P)",
                min_value=5.0,
                max_value=145.0,
                value=50.0,
                step=0.1,
                key="shap_p"
            )
 
            potassium = st.number_input(
                "Potassium (K)",
                min_value=5.0,
                max_value=205.0,
                value=50.0,
                step=0.1,
                key="shap_k"
            )
 
    with col2:
 
        with st.container(border=True):
 
            st.markdown(
                '<div class="input-group-title">Climate Conditions</div>',
                unsafe_allow_html=True
            )
 
            temperature = st.number_input(
                "Temperature (°C)",
                min_value=8.0,
                max_value=44.0,
                value=25.0,
                step=0.1,
                key="shap_temperature"
            )
 
            humidity = st.number_input(
                "Humidity (%)",
                min_value=14.0,
                max_value=100.0,
                value=70.0,
                step=0.1,
                key="shap_humidity"
            )
 
            rainfall = st.number_input(
                "Rainfall (mm)",
                min_value=20.0,
                max_value=299.0,
                value=100.0,
                step=0.1,
                key="shap_rainfall"
            )
 
    with col3:
 
        with st.container(border=True):
 
            st.markdown(
                '<div class="input-group-title">Soil Condition</div>',
                unsafe_allow_html=True
            )
 
            ph = st.number_input(
                "Soil pH",
                min_value=3.5,
                max_value=9.9,
                value=6.5,
                step=0.1,
                key="shap_ph"
            )
 
            st.markdown("""
<div class="info-note">
<b>SHAP explanation</b><br>
The analysis shows how each input feature contributes
to the selected model prediction.
</div>
""", unsafe_allow_html=True)
 
    spacer()
 
 
    # -----------------------------------------------------
    # EXPLAIN BUTTON
    # -----------------------------------------------------
 
    explain_clicked = st.button(
        "🔍 Explain Prediction",
        use_container_width=True
    )
 
 
    if explain_clicked:
 
        # Keep feature names identical to training dataset
        input_data = pd.DataFrame([{
            "N": nitrogen,
            "P": phosphorus,
            "K": potassium,
            "temperature": temperature,
            "humidity": humidity,
            "ph": ph,
            "rainfall": rainfall
        }])
 
 
        # -------------------------------------------------
        # RANDOM FOREST PREDICTION
        # -------------------------------------------------
 
        prediction = random_forest_model.predict(
            input_data
        )[0]
 
        probabilities = random_forest_model.predict_proba(
            input_data
        )[0]
 
        class_names = random_forest_model.classes_
 
        predicted_class_index = list(
            class_names
        ).index(prediction)
 
        prediction_score = (
            probabilities[predicted_class_index] * 100
        )
 
 
        # -------------------------------------------------
        # SHAP ANALYSIS
        # -------------------------------------------------
 
        import shap
 
        explainer = shap.TreeExplainer(
            random_forest_model
        )
 
        shap_values = explainer.shap_values(
            input_data
        )
 
 
        # Handle different SHAP output formats
        if isinstance(shap_values, list):
 
            feature_contributions = shap_values[
                predicted_class_index
            ][0]
 
        elif len(shap_values.shape) == 3:
 
            feature_contributions = shap_values[
                0,
                :,
                predicted_class_index
            ]
 
        else:
 
            feature_contributions = shap_values[0]
 
 
        feature_names = list(input_data.columns)
 
        explanation_df = pd.DataFrame({
            "Feature": feature_names,
            "Input Value": input_data.iloc[0].values,
            "SHAP Value": feature_contributions
        })
 
 
        explanation_df["Impact"] = explanation_df[
            "SHAP Value"
        ].apply(
            lambda value:
            "Supports prediction"
            if value > 0
            else "Pushes away from prediction"
        )
 
 
        explanation_df["Absolute Impact"] = (
            explanation_df["SHAP Value"].abs()
        )
 
        explanation_df = explanation_df.sort_values(
            "Absolute Impact",
            ascending=False
        )
 
 
        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------
 
        st.divider()
 
        section_header(
            "Prediction Explained",
            "Random Forest prediction and feature-level contribution."
        )
 
        col1, col2 = st.columns(2)
 
        with col1:
 
            st.markdown(f"""
<div class="result-box">
<div class="result-label">Predicted Crop</div>
<div class="result-crop">{prediction.title()}</div>
</div>
""", unsafe_allow_html=True)
 
        with col2:
 
            st.metric(
                "Model Score",
                f"{prediction_score:.2f}%"
            )
 
        spacer()
 
 
        # -------------------------------------------------
        # FEATURE CONTRIBUTION CHART
        # -------------------------------------------------
 
        section_header(
            "Feature Contribution",
            "Positive values support the predicted crop, while "
            "negative values push the prediction away from it."
        )
 
        chart_df = explanation_df[
            ["Feature", "SHAP Value"]
        ].copy()
 
        chart_df = chart_df.set_index(
            "Feature"
        )
 
        st.bar_chart(
            chart_df,
            horizontal=True,
            color="#1f6b43"
        )
 
        spacer()
 
 
        # -------------------------------------------------
        # DETAILED CONTRIBUTIONS
        # -------------------------------------------------
 
        section_header("Detailed Contributions")
 
        display_df = explanation_df[
            [
                "Feature",
                "Input Value",
                "SHAP Value",
                "Impact"
            ]
        ].copy()
 
        display_df["SHAP Value"] = display_df[
            "SHAP Value"
        ].round(4)
 
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
 
 
        # -------------------------------------------------
        # TOP INFLUENCE
        # -------------------------------------------------
 
        strongest_feature = explanation_df.iloc[0]
 
        spacer()
 
        st.info(
            f"The feature with the strongest contribution "
            f"for this prediction is **{strongest_feature['Feature']}**."
        )
 
        st.caption(
            "SHAP values explain the model's prediction for this "
            "input. They do not represent a direct causal effect "
            "on crop growth or agricultural outcomes."
        )
 
 
# =========================================================
# WHAT-IF ANALYSIS
# =========================================================
 
elif page == "🧪 What-If Analysis":
 
    page_header(
        "What-If Analysis",
        "Explore how changing environmental conditions can affect "
        "the model prediction."
    )
 
    st.info(
        "What-If analysis will be added here."
    )
 
 
# =========================================================
# PREDICTION HISTORY
# =========================================================
 
elif page == "📜 Prediction History":
 
    page_header(
        "Prediction History",
        "Previous crop predictions will be displayed here."
    )
 
    st.info(
        "Prediction history will be connected to the application "
        "database later."
    )
 
 
# =========================================================
# DATASET & EDA
# =========================================================
 
elif page == "📈 Dataset & EDA":
 
    page_header(
        "Dataset & Exploratory Data Analysis",
        "Explore the dataset and visualizations used during "
        "model development."
    )
 
    st.info(
        "Dataset preview and EDA visualizations will be added here."
    )
 
 
# =========================================================
# TEAM
# =========================================================
 
elif page == "👥 Team":
 
    page_header(
        "Project Team",
        "CropCompass — Machine Learning Project"
    )
 
    st.info(
        "Team details will be added here."
    )
 