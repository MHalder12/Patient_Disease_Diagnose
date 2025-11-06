import streamlit as st

class DiseaseUI:
    @staticmethod
    def apply_custom_css():
        st.markdown("""
            <style>
            /* Background Gradient */
            .stApp {
                background: linear-gradient(120deg, #3f5a66 0%, #3d5275 100%);
                color: #ced1d6;
                font-family: 'Poppins', sans-serif;
            }

            h1 {
                color: #d7dce0;
                text-align: center;
                font-weight: 800 !important;
                text-shadow: 1px 1px 3px #ffffff;
            }

            .section-title {
                font-size: 22px;
                font-weight: 700;
                color: #d7dce0;
                border-bottom: 3px solid #0080ff;
                margin-bottom: 10px;
            }

            div.stButton > button {
                background-color: #007bff;
                color: white;
                border-radius: 8px;
                height: 50px;
                width: 100%;
                font-size: 18px;
                transition: all 0.3s ease;
            }
            div.stButton > button:hover {
                background-color: #0056b3;
                transform: scale(1.03);
            }

            .success {
                background-color: #e3fcef;
                border-left: 6px solid #28a745;
                padding: 15px;
                border-radius: 10px;
                font-weight: 600;
            }

            .warning {
                background-color: #fff3cd;
                border-left: 6px solid #ffcc00;
                padding: 15px;
                border-radius: 10px;
            }
            </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def patient_form(encoders):
        """Builds and returns all patient input data as a dictionary."""
        st.title("🩺 Patient Disease Prediction App")

        # --- Patient Info ---
        st.markdown("<div class='section-title'>👤 Patient Information</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", 1, 100, 30)
        with col2:
            gender = st.selectbox("Gender", encoders["Gender"].classes_)

        # --- Vital Signs ---
        st.markdown("<div class='section-title'>🌡️ Vital Signs</div>", unsafe_allow_html=True)
        col3, col4, col5 = st.columns(3)
        with col3:
            body_temp = st.number_input("Body Temperature (°C)", 34.0, 42.0, 36.8)
        with col4:
            heart_rate = st.number_input("Heart Rate (bpm)", 40, 180, 80)
        with col5:
            blood_pressure = st.selectbox("Blood Pressure", ["Normal", "Low", "High"])

        # --- Symptoms ---
        st.markdown("<div class='section-title'>🤧 Symptoms</div>", unsafe_allow_html=True)
        col6, col7, col8 = st.columns(3)
        with col6:
            cough = st.selectbox("Cough", ["None", "Mild", "Severe"])
        with col7:
            headache = st.selectbox("Headache", ["None", "Mild", "Severe"])
        with col8:
            fatigue = st.selectbox("Fatigue", ["None", "Moderate", "High"])

        # --- Lab Values ---
        st.markdown("<div class='section-title'>🧬 Lab Values</div>", unsafe_allow_html=True)
        col9, col10 = st.columns(2)
        with col9:
            wbc = st.number_input("WBC Count (x10⁹/L)", 2.0, 20.0, 7.0)
        with col10:
            sugar = st.number_input("Sugar Level (mg/dL)", 50, 300, 100)

        # Return data dictionary
        return {
            "Age": age,
            "Gender": gender,
            "Body_Temperature": body_temp,
            "Cough": cough,
            "Headache": headache,
            "Fatigue": fatigue,
            "Blood_Pressure": blood_pressure,
            "Heart_Rate": heart_rate,
            "WBC_Count": wbc,
            "Sugar_Level": sugar,
        }

    @staticmethod
    def show_result(result, healthy=False):
        """Displays the prediction result with styled feedback."""
        if healthy:
            st.markdown(f"<div class='success'>🩺 The patient appears **Healthy** ({result}).</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='warning'>🧠 Predicted Disease: <b>{result}</b></div>", unsafe_allow_html=True)

    @staticmethod
    def show_footer():
        st.markdown("""
            ---
            ### 💡 About This App
            Built with ❤️ using **Streamlit**  
            Developed by Madhumanti  
            🔗 For research and educational use only.
        """)
