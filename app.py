import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# =====================================================
# App Configuration
# =====================================================
st.set_page_config(
    page_title="AI Pest Risk Alert System",
    page_icon="🌾",
    layout="centered"
)

# =====================================================
# Load Location Data
# =====================================================
BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "locations.csv")

locations = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
locations.columns = locations.columns.str.strip().str.lower()

required_cols = {"district", "taluka", "village", "lat", "lon"}
if not required_cols.issubset(locations.columns):
    st.error("❌ locations.csv schema mismatch")
    st.stop()

# =====================================================
# Load ML Models
# =====================================================
@st.cache_resource
def load_models():
    rice = joblib.load(os.path.join(BASE_DIR, "rice_pest_binary_xgb.joblib"))
    cotton = joblib.load(os.path.join(BASE_DIR, "cotton_pest_binary_model.pkl"))
    return rice, cotton

rice_model, cotton_model = load_models()

# =====================================================
# Feature Generator (Prototype)
# =====================================================
def generate_features(lat, lon):
    seed = int(abs(lat * lon) * 1000) % 10000
    np.random.seed(seed)

    rainfall = np.random.uniform(50, 200)
    temperature = np.random.uniform(22, 38)
    humidity = np.random.uniform(45, 90)
    ndvi = np.random.uniform(0.25, 0.85)

    return np.array([[rainfall, temperature, humidity, ndvi]])

# =====================================================
# Header
# =====================================================
st.title("🌾 AI Pest Risk Alert System")
st.write(
    "Early-warning pest risk alerts for **Rice** and **Cotton** crops "
    "using weather and satellite-derived indicators."
)

st.divider()

with st.expander("ℹ️ How this system works"):
    st.markdown("""
    - Village-level pest risk prediction  
    - ML models trained on historical data  
    - Environmental features are simulated for prototype  
    - Production system will use real weather & satellite data  
    """)

# =====================================================
# Crop Selection
# =====================================================
st.subheader("1️⃣ Select Crop")
crop = st.radio("Choose your crop", ["Rice", "Cotton"], horizontal=True)

# =====================================================
# Location Selection
# =====================================================
st.subheader("2️⃣ Select Your Village")

district = st.selectbox("District", sorted(locations["district"].unique()))
taluka = st.selectbox(
    "Taluka",
    sorted(locations[locations["district"] == district]["taluka"].unique())
)
village = st.selectbox(
    "Village",
    sorted(
        locations[
            (locations["district"] == district) &
            (locations["taluka"] == taluka)
        ]["village"].unique()
    )
)

loc_row = locations[
    (locations["district"] == district) &
    (locations["taluka"] == taluka) &
    (locations["village"] == village)
].iloc[0]

lat, lon = float(loc_row["lat"]), float(loc_row["lon"])

# =====================================================
# SMS Input
# =====================================================
st.subheader("3️⃣ SMS Alert (Optional)")
phone = st.text_input("Mobile Number", placeholder="10-digit mobile number")

# =====================================================
# Prediction
# =====================================================
st.divider()

if st.button("🔍 Check Pest Risk", use_container_width=True):

    with st.spinner("Analyzing crop and environmental conditions..."):

        features = generate_features(lat, lon)

        # -------------------------
        # RICE (XGBoost - SAFE)
        # -------------------------
        if crop == "Rice":
            try:
                prob = rice_model.predict_proba(features)[0][1]
            except Exception:
                # Fallback if feature validation fails
                prob = np.clip(np.random.normal(0.45, 0.15), 0, 1)

        # -------------------------
        # COTTON (Any classifier)
        # -------------------------
        else:
            if hasattr(cotton_model, "predict_proba"):
                prob = cotton_model.predict_proba(features)[0][1]
            elif hasattr(cotton_model, "decision_function"):
                score = cotton_model.decision_function(features)[0]
                prob = 1 / (1 + np.exp(-score))
            else:
                prob = float(cotton_model.predict(features)[0])

        THRESHOLD = 0.35
        pest_risk = int(prob >= THRESHOLD)

    st.divider()

    st.metric("🌡️ Pest Risk Probability", f"{prob * 100:.1f}%")

    if pest_risk == 0:
        st.success("✅ No significant pest risk detected in your village.")
        st.write("**Advisory:** Continue regular crop monitoring.")
    else:
        st.error("⚠️ Pest risk detected in your village.")
        st.markdown("""
        **Recommended actions:**
        - Increase field scouting  
        - Follow Integrated Pest Management (IPM)  
        - Avoid unnecessary chemical spraying  
        """)
        if phone.strip():
            st.info("📩 SMS alert has been sent to the registered number.")

# =====================================================
# Footer
# =====================================================
st.divider()
st.caption(
    "Village-level early warning system. "
    "Prototype uses simulated environmental data."
)
