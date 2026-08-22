import streamlit as st
import pandas as pd
import joblib


# ========================================================
# PAGE CONFIGURATION
# ========================================================

st.set_page_config(
    page_title="Employee Attrition Predictor",
    page_icon="👨‍💼",
    layout="centered"
)


# ========================================================
# SESSION STATE
# ========================================================

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "blocked" not in st.session_state:
    st.session_state.blocked = False

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "prediction_data" not in st.session_state:
    st.session_state.prediction_data = []


# ========================================================
# MENU
# ========================================================

menu = st.radio(
    "",
    [
        "🏠 Home",
        "🔐 Admin Panel"
    ]
)


# ========================================================
# CSS
# ========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #74ebd5, #ACB6E5);
}

h1 {
    text-align: center;
    color: #0B3D91;
    font-weight: bold;
}

div.stButton > button {
    width: 100%;
    background: #0B3D91;
    color: white;
    font-size: 18px;
    border-radius: 10px;
    height: 50px;
}

div.stButton > button:hover {
    background: #1E90FF;
    color: white;
}

.result {
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ========================================================
# SIDEBAR
# ========================================================

st.sidebar.image(
    "https://img.icons8.com/color/96/businessman.png",
    width=100
)

st.sidebar.title("Employee Attrition")


# ========================================================
# HOME PAGE
# ========================================================

if menu == "🏠 Home":

    st.sidebar.info("""
    Fill employee details and click **Predict**
    to know whether the employee is likely to leave.
    """)

    st.title("👨‍💼 Employee Attrition Prediction")

    st.write(
        "Enter employee details to predict whether "
        "the employee will leave the company."
    )

    # ----------------------------------------------------
    # INPUTS
    # ----------------------------------------------------

    Age = st.number_input(
        "Age",
        min_value=18,
        max_value=65,
        value=25
    )

    MonthlyIncome = st.number_input(
        "Monthly Income",
        min_value=0,
        value=30000
    )

    DistanceFromHome = st.number_input(
        "Distance From Home",
        min_value=0,
        value=5
    )

    YearsAtCompany = st.number_input(
        "Years At Company",
        min_value=0,
        value=2
    )

    JobSatisfaction = st.selectbox(
        "Job Satisfaction",
        [1, 2, 3, 4]
    )

    OverTime = st.selectbox(
        "OverTime",
        ["Yes", "No"]
    )


    # ----------------------------------------------------
    # CONVERT OVERTIME
    # ----------------------------------------------------

    overtime_text = OverTime

    OverTime = 1 if OverTime == "Yes" else 0


    # ----------------------------------------------------
    # USER INPUT DATAFRAME
    # ----------------------------------------------------

    user_input = pd.DataFrame({
        "Age": [Age],
        "MonthlyIncome": [MonthlyIncome],
        "DistanceFromHome": [DistanceFromHome],
        "YearsAtCompany": [YearsAtCompany],
        "JobSatisfaction": [JobSatisfaction],
        "OverTime": [OverTime]
    })


    # ----------------------------------------------------
    # LOAD MODEL
    # ----------------------------------------------------

    try:

        model = joblib.load(
            "employee_attrition_model.pkl"
        )

    except Exception:

        st.error(
            "❌ employee_attrition_model.pkl "
            "could not be loaded."
        )

        st.stop()


    # ====================================================
    # PREDICT
    # ====================================================

    if st.button("🔍 Predict"):

        prediction = model.predict(user_input)

        prediction_value = int(prediction[0])


        # ------------------------------------------------
        # PREDICTION TEXT
        # ------------------------------------------------

        if prediction_value == 1:

            prediction_text = "Likely to Leave"

            st.markdown("""
            <div class='result'
            style='background:#ffcccc;color:#b30000;'>
            ⚠️ Employee is likely to leave the company.
            </div>
            """, unsafe_allow_html=True)

        else:

            prediction_text = "Likely to Stay"

            st.markdown("""
            <div class='result'
            style='background:#ccffcc;color:#006600;'>
            ✅ Employee is likely to stay in the company.
            </div>
            """, unsafe_allow_html=True)


        # ------------------------------------------------
        # SAVE PREDICTION
        # ------------------------------------------------

        employee_record = {
            "Age": Age,
            "Monthly Income": MonthlyIncome,
            "Distance From Home": DistanceFromHome,
            "Years At Company": YearsAtCompany,
            "Job Satisfaction": JobSatisfaction,
            "OverTime": overtime_text,
            "Prediction": prediction_text
        }

        st.session_state.prediction_data.append(
            employee_record
        )


# ========================================================
# ADMIN PANEL
# ========================================================

elif menu == "🔐 Admin Panel":

    # ====================================================
    # IF USER IS ALREADY LOGGED IN
    # ====================================================

    if st.session_state.admin_logged_in:

        st.success("✅ Admin Login Successful!")

        st.title("📊 Admin Dashboard")

        st.write(
            "Here you can view employee prediction records."
        )


        # ------------------------------------------------
        # CHECK DATA
        # ------------------------------------------------

        if len(st.session_state.prediction_data) == 0:

            st.info(
                "📭 No employee prediction data available yet."
            )

        else:

            # --------------------------------------------
            # CONVERT DATA TO DATAFRAME
            # --------------------------------------------

            prediction_df = pd.DataFrame(
                st.session_state.prediction_data
            )


            # --------------------------------------------
            # DASHBOARD METRICS
            # --------------------------------------------

            total = len(prediction_df)

            leave_count = len(
                prediction_df[
                    prediction_df["Prediction"]
                    == "Likely to Leave"
                ]
            )

            stay_count = len(
                prediction_df[
                    prediction_df["Prediction"]
                    == "Likely to Stay"
                ]
            )


            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "👥 Total Predictions",
                    total
                )

            with col2:
                st.metric(
                    "⚠️ Likely to Leave",
                    leave_count
                )

            with col3:
                st.metric(
                    "✅ Likely to Stay",
                    stay_count
                )


            # --------------------------------------------
            # EMPLOYEE DATA
            # --------------------------------------------

            st.subheader(
                "👨‍💼 Employee Prediction Data"
            )

            st.dataframe(
                prediction_df,
                use_container_width=True
            )


            # --------------------------------------------
            # DOWNLOAD DATA
            # --------------------------------------------

            csv = prediction_df.to_csv(
                index=False
            )

            st.download_button(
                label="⬇️ Download Employee Data",
                data=csv,
                file_name="employee_predictions.csv",
                mime="text/csv",
                use_container_width=True
            )


        # ------------------------------------------------
        # LOGOUT
        # ------------------------------------------------

        if st.button("🚪 Logout"):

            st.session_state.admin_logged_in = False

            st.rerun()


    # ====================================================
    # LOGIN PAGE
    # ====================================================

    else:

        # ------------------------------------------------
        # CHECK BLOCKED
        # ------------------------------------------------

        if st.session_state.blocked:

            st.error("🚫 Access Blocked!")

            st.warning(
                "You entered the incorrect password "
                "3 times."
            )

            st.info(
                "Please contact the administrator "
                "for access."
            )

            st.stop()


        # ------------------------------------------------
        # LOGIN
        # ------------------------------------------------

        st.title("🔐 Administrator Login")

        password = st.text_input(
            "Enter Administrator Password",
            type="password"
        )


        if st.button(
            "🔓 Login",
            use_container_width=True
        ):

            # ============================================
            # CORRECT PASSWORD
            # ============================================

            if password.strip() == "manager123":

                st.session_state.attempts = 0

                st.session_state.admin_logged_in = True

                st.success(
                    "✅ Access Granted!"
                )

                st.rerun()


            # ============================================
            # WRONG PASSWORD
            # ============================================

            else:

                st.session_state.attempts += 1

                remaining = (
                    3 - st.session_state.attempts
                )


                # ----------------------------------------
                # BLOCK AFTER 3 ATTEMPTS
                # ----------------------------------------

                if st.session_state.attempts >= 3:

                    st.session_state.blocked = True

                    st.error(
                        "🚫 Access blocked after "
                        "3 incorrect attempts."
                    )

                    st.info(
                        "Please contact the administrator."
                    )

                    st.stop()


                else:

                    st.error(
                        "❌ Incorrect Password!"
                    )

                    st.warning(
                        f"⚠️ {remaining} "
                        f"attempt(s) remaining."
                    )