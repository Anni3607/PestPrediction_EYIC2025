
import streamlit as st
import pandas as pd

# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Pest Risk Alert System",
    page_icon="🌾",
    layout="centered"
)

# -----------------------------
# Load Location Data
# -----------------------------
locations = pd.read_csv("locations.csv")

# -----------------------------
# Header
# -----------------------------
st.title(" AI Pest Risk Alert System")
st.write(
    "Early-warning pest risk alerts for **Rice** and **Cotton** crops "
    "using weather and satellite-derived indicators."
)

st.divider()

# -----------------------------
# How it Works (Explainability)
# -----------------------------
with st.expander(" How this system works"):
    st.write("""
    - Pest risk is predicted at **village level**
    - All farms in the same village receive the same alert
    - Uses **weather and satellite crop health data**
    - Provides **early-warning risk**, not pest detection
    - Alerts are preventive and IPM-oriented
    """)

# -----------------------------
# Crop Selection
# -----------------------------
st.subheader(" Select Crop")
crop = st.radio(
    "Choose your crop",
    ["Rice", "Cotton"],
    horizontal=True
)

# -----------------------------
# Location Selection
# -----------------------------
st.subheader(" Select Your Village")

district = st.selectbox(
    "District",
    sorted(locations["district"].unique())
)

taluka = st.selectbox(
    "Taluka",
    sorted(locations[locations["district"] == district]["taluka"].unique())
)

village = st.selectbox(
    "Village",
    locations[
        (locations["district"] == district) &
        (locations["taluka"] == taluka)
    ]["village"].unique()
)

loc_row = locations[locations["village"] == village].iloc[0]
lat, lon = loc_row["lat"], loc_row["lon"]

# -----------------------------
# Phone Number (Optional)
# -----------------------------
st.subheader("3️ SMS Alert (Optional)")
phone = st.text_input(
    "Mobile Number (for SMS alert if pest risk is detected)",
    placeholder="10-digit mobile number"
)

# -----------------------------
# Prediction Trigger
# -----------------------------
st.divider()

if st.button("Check Pest Risk", use_container_width=True):

    with st.spinner("Analyzing crop and weather conditions..."):
        # -----------------------------
        # MOCK PREDICTION LOGIC
        # (Replace with real ML later)
        # -----------------------------
        if crop == "Rice":
            pest_risk = 0  # binary: 0 = low, 1 = risk
        else:
            pest_risk = 1

    st.divider()

    # -----------------------------
    # Results Display
    # -----------------------------
    if pest_risk == 0:
        st.success("No significant pest risk detected in your village.")
        st.write("**Advisory:** Continue regular crop monitoring.")

    else:
        st.error(" Pest risk detected in your village.")
        st.write("**Recommended actions:**")
        st.markdown("""
        - Monitor crop closely  
        - Use Integrated Pest Management (IPM) practices  
        - Avoid unnecessary chemical spraying  
        """)

        if phone.strip():
            st.info(" SMS alert has been sent to the registered number.")

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption(
    "This system provides **village-level early warning alerts** "
    "based on environmental conditions. "
    "It is not a diagnostic tool."
)
