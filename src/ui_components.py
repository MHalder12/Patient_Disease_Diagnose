import streamlit as st

class DiseaseUI:
    @staticmethod
    def apply_modern_theme():
        """Apply a professional hospital-style theme"""
        st.markdown("""
        <style>
            /* General App Styling */
            .stApp {
                background-color: #f7fbff;  /* Soft blue-white */
                font-family: 'Poppins', sans-serif;
                color: #000;
            }

            /* Headers */
            h1, h2, h3 {
                color: #004080 !important;
                font-weight: 700;
                text-align: center;
            }

            /* Section Titles */
            .section-title {
                font-size: 22px;
                font-weight: 700;
                color: #0066cc;
                border-left: 5px solid #0099ff;
                padding-left: 10px;
                margin-top: 25px;
                margin-bottom: 10px;
            }

            /* Form Labels */
            label, .stSelectbox label, .stNumberInput label, .stSlider label {
                color: #000 !important;
                font-weight: 600;
            }

            /* Input Boxes */
            .stTextInput, .stNumberInput, .stSelectbox, .stSlider {
                border-radius: 8px;
            }

            /* Buttons */
            div.stButton > button {
                background-color: #0078d7;
                color: white;
                border-radius: 8px;
                height: 50px;
                font-size: 17px;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0px 2px 6px rgba(0,0,0,0.2);
            }

            div.stButton > button:hover {
                background-color: #005bb5;
                transform: scale(1.03);
            }

            /* Result Styling */
            .result-box {
                background-color: #d4edda;           /* Soft green */
                border-left: 8px solid #155724;      /* Dark green accent */
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                font-size: 20px;
                color: #0f3d0f;                      /* Darker green font */
                font-weight: 700;                    /* Bold */
            }

            .warning-box {
                background-color: #fff3cd;           /* Light yellow */
                border-left: 8px solid #856404;      /* Dark amber */
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                font-size: 20px;
                color: #4a3b00;                      /* Darker brown */
                font-weight: 700;
            }

            /* Footer */
            .footer {
                text-align: center;
                font-size: 14px;
                margin-top: 40px;
                color: #444;
            }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def patient_form(encoders):
        """Display input form for symptoms"""
        st.title("🏥 AI-Powered Disease Diagnosis System")
        st.markdown("<div style='text-align:center; color:#666;'>Enter patient details below for a quick diagnosis.</div>", unsafe_allow_html=True)

        # Patient Info
        st.markdown("<div class='section-title'>👤 Patient Details</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", 1, 100, 30)
        with col2:
            gender = st.selectbox("Gender", encoders["Gender"].classes_)

        # Vitals
        st.markdown("<div class='section-title'>🌡️ Vital Signs</div>", unsafe_allow_html=True)
        col3, col4, col5 = st.columns(3)
        with col3:
            body_temp = st.number_input("Body Temperature (°C)", 34.0, 42.0, 36.8)
        with col4:
            heart_rate = st.number_input("Heart Rate (bpm)", 40, 180, 80)
        with col5:
            blood_pressure = st.selectbox("Blood Pressure", ["Normal", "Low", "High"])

        # Symptoms
        st.markdown("<div class='section-title'>🤧 Symptoms</div>", unsafe_allow_html=True)
        col6, col7, col8 = st.columns(3)
        with col6:
            cough = st.selectbox("Cough", ["None", "Mild", "Severe"])
        with col7:
            headache = st.selectbox("Headache", ["None", "Mild", "Severe"])
        with col8:
            fatigue = st.selectbox("Fatigue", ["None", "Moderate", "High"])

        # Lab Values
        st.markdown("<div class='section-title'>🧬 Laboratory Results</div>", unsafe_allow_html=True)
        col9, col10 = st.columns(2)
        with col9:
            wbc = st.number_input("WBC Count (x10⁹/L)", 2.0, 20.0, 7.0)
        with col10:
            sugar = st.number_input("Sugar Level (mg/dL)", 50, 300, 100)

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
            "Sugar_Level": sugar
        }

    @staticmethod
    def show_result(predicted_disease, is_healthy=False):
        """Display the result in a styled box"""
        if is_healthy:
            st.markdown(f"<div class='result-box'>✅ The patient appears **Healthy**</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='warning-box'>⚠️ Predicted Disease: <b>{predicted_disease}</b></div>", unsafe_allow_html=True)

    @staticmethod
    def footer():
        st.markdown("""
            <div class='footer'>
            © 2025 AI Disease Predictor | Built with ❤️ using Streamlit
            </div>
        """, unsafe_allow_html=True)
