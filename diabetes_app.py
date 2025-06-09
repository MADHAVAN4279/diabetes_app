
import streamlit as st
import streamlit_authenticator as stauth
import numpy as np
import joblib
import pandas as pd

# --- Authentication Setup ---
# Create hashed passwords (only once, or use pre-generated values)
hashed_passwords = stauth.Hasher(['adminpass', 'userpass']).generate()

credentials = {
    "usernames": {
        "admin": {
            "name": "Admin User",
            "password": hashed_passwords[0],
            "role": "admin"
        },
        "user": {
            "name": "General User",
            "password": hashed_passwords[1],
            "role": "user"
        }
    }
}

authenticator = stauth.Authenticate(
    credentials, "cookie_name", "signature_key", cookie_expiry_days=1
)

# --- Login UI ---
name, auth_status, username = authenticator.login("Login", "main")

# --- Logout Button ---
if auth_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Logged in as: {name} ({credentials['usernames'][username]['role'].capitalize()})")

    role = credentials['usernames'][username]['role']

    if role == "admin":
        st.title("🔧 Admin Dashboard")

        st.subheader("User Management")
        st.write("➕ Add/Remove Users (demo only)")

        st.subheader("Model Configuration")
        model_type = st.radio("Choose Model Type", ["Binary Classification", "Multi-class Classification"])
        st.success(f"Model set to: {model_type}")

        st.subheader("Dataset Upload")
        uploaded_file = st.file_uploader("Upload new dataset (CSV)", type="csv")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write("Preview of uploaded dataset:")
            st.dataframe(df.head())

    elif role == "user":
        st.title("🩺 Diabetes Prediction")

        preg = st.number_input("Pregnancies", 0.0, 20.0, 1.0)
        glucose = st.number_input("Glucose", 0.0, 200.0, 120.0)
        bp = st.number_input("Blood Pressure", 0.0, 122.0, 70.0)
        skin = st.number_input("Skin Thickness", 0.0, 100.0, 20.0)
        insulin = st.number_input("Insulin", 0.0, 900.0, 80.0)
        bmi = st.number_input("BMI", 0.0, 67.0, 28.0)
        dpf = st.number_input("Diabetes Pedigree Function", 0.0, 2.5, 0.5)
        age = st.number_input("Age", 1.0, 100.0, 33.0)

        model = joblib.load("diabetes_model.pkl")

        if st.button("Predict"):
            features = np.array([[preg, glucose, bp, skin, insulin, bmi, dpf, age]])
            prediction = model.predict(features)[0]
            probability = model.predict_proba(features)[0][prediction]

            if prediction == 1:
                st.error(f"⚠️ High risk of diabetes (Confidence: {probability:.2f})")
            else:
                st.success(f"✅ Low risk of diabetes (Confidence: {probability:.2f})")

            st.markdown("### Recommendations:")
            st.markdown("- Maintain healthy weight\n- Exercise regularly\n- Follow a balanced diet")

else:
    st.warning("Please enter a valid username and password.")
