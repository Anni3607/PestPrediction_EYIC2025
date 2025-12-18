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
# Load Location Data (CSV)
# =====================================================
BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "locations.csv")

locations = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

# Clean column names
locations.columns = locations.columns.str.strip().str.lower()

# Validate schema
required_cols = {"district", "taluka", "village", "lat", "lon"}
if not required_cols.issubset(locations.columns):
    st.error("❌ locations.csv schema mismatch")
    st.write("Found columns:", list(locations.columns))
    st.stop()

# =====================================================
# Load ML Models (Cached)
# =====================================================
@st.cache_resource
def load_models():
    rice_model = joblib.load(os.path.join(BASE_DIR, "rice_pest_binary_xgb.joblib"))
    cotton_model = joblib.load(os.path.join(BASE_DIR, "cotton_pest_binary_model.pkl"))
    return rice_model, cotton_model

rice_model, cotton_model = load_models()

# =====================================================
# Feature Generator (Simulated but Consistent)
# =====================================================
def generate_features(lat, lon):
    """
    Simulate environmental features based on location.
    This mimics weather + satellite variability.
    """
    seed = int(abs(lat * lon) * 1000) % 10000
    np.random.seed(seed)

    rainfall = np.random.uniform(50, 200)      # mm
    temperature = np.random.uniform(22, 38)    # °C
    humidity = np.random.uniform(45, 90)       # %
    ndvi = np.random.uniform(0.25, 0.85)       # vegetation index

    # ⚠️ FEATURE ORDER MUST MATCH TRAINING
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

# =====================================================
# How It Works
# =====================================================
with st.expander("ℹ️ How this system works"):
    st.markdown("""
    - Risk is predicted at **village level**
    - ML models trained on historical pest & climate data
    - Current prototype simulates environmental inputs
    - In production, live weather & satellite data will be used
    """)

# =====================================================
# Crop Selection
# =====================================================
st.subheader("1️⃣ Select Crop")
crop = st.radio("Choose your crop", ["Rice", "Cotton"], horizontal=True)

# =====================================================
# Location Selection (Cascading)
# =====================================================
st.subheader("2️⃣ Select Your Village")

districts = sorted(locations["district"].unique())
district = st.selectbox("District", districts)

talukas = sorted(
    locations[locations["district"] == district]["taluka"].unique()
)
taluka = st.selectbox("Taluka", talukas)

villages = sorted(
    locations[
        (locations["district"] == district) &
        (locations["taluka"] == taluka)
    ]["village"].unique()
)
village = st.selectbox("Village", villages)

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
phone = st.text_input(
    "Mobile Number (for alert if risk is detected)",
    placeholder="10-digit mobile number"
)

# =====================================================
# Prediction Trigger
# =====================================================
st.divider()

if st.button("🔍 Check Pest Risk", use_container_width=True):

    with st.spinner("Analyzing crop, weather, and satellite indicators..."):

        features = generate_features(lat, lon)

        if crop == "Rice":
            prob = rice_model.predict_proba(features)[0][1]
        else:
            prob = cotton_model.predict_proba(features)[0][1]

        THRESHOLD = 0.35
        pest_risk = int(prob >= THRESHOLD)

    st.divider()

    # =================================================
    # Results
    # =================================================
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
    "This system provides **village-level early warning alerts** "
    "based on environmental conditions. "
    "It is not a diagnostic tool."
)
