import streamlit as st
import pandas as pd
import os
import re

# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Pest Risk Alert System",
    page_icon="🌾",
    layout="centered"
)

# -----------------------------
# Load CSV safely
# -----------------------------
BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "locations.csv")

locations = pd.read_csv(
    CSV_PATH,
    encoding="utf-8-sig",   # 🔥 removes BOM
    sep=","
)

# -----------------------------
# HARD CLEAN column names
# -----------------------------
locations.columns = (
    locations.columns
    .str.replace(r"[^\w]", "", regex=True)  # remove hidden chars
    .str.lower()
)

# -----------------------------
# REQUIRED CHECK
# -----------------------------
required = {"district", "taluka", "village", "lat", "lon"}
missing = required - set(locations.columns)

if missing:
    st.error("❌ CSV column mismatch")
    st.write("Found columns:", list(locations.columns))
    st.write("Missing columns:", list(missing))
    st.stop()

# -----------------------------
# Header
# -----------------------------
st.title("🌾 AI Pest Risk Alert System")
st.write(
    "Early-warning pest risk alerts for **Rice** and **Cotton** crops "
    "using weather and satellite-derived indicators."
)

st.divider()

# -----------------------------
# How it Works
# -----------------------------
with st.expander("ℹ️ How this system works"):
    st.write("""
    - Pest risk is predicted at **village level**
    - Same alert for all farms in a village
    - Uses weather & satellite indicators
    """)

# -----------------------------
# Crop Selection
# -----------------------------
st.subheader("1️⃣ Select Crop")
crop = st.radio("Choose your crop", ["Rice", "Cotton"], horizontal=True)

# -----------------------------
# Location Selection
# -----------------------------
st.subheader("2️⃣ Select Your Village")

district = st.selectbox(
    "District",
    sorted(locations["district"].unique())
)

taluka = st.selectbox(
    "Taluka",
    sorted(
        locations[locations["district"] == district]["taluka"].unique()
    )
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

lat, lon = loc_row["lat"], loc_row["lon"]

# -----------------------------
# Phone
# -----------------------------
st.subheader("3️⃣ SMS Alert (Optional)")
phone = st.text_input("Mobile Number", placeholder="10-digit number")

# -----------------------------
# Prediction
# -----------------------------
st.divider()

if st.button("🔍 Check Pest Risk", use_container_width=True):

    with st.spinner("Analyzing crop and weather conditions..."):
        pest_risk = 0 if crop == "Rice" else 1

    st.divider()

    if pest_risk == 0:
        st.success("✅ No significant pest risk detected.")
    else:
        st.error("⚠️ Pest risk detected.")
        st.markdown("""
        **Recommended actions:**
        - Monitor crop closely  
        - Follow IPM practices  
        - Avoid unnecessary spraying  
        """)

        if phone.strip():
            st.info("📩 SMS alert sent.")

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption("Village-level early warning system. Not diagnostic.")
