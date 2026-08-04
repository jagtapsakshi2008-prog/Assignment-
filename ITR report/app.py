
import streamlit as st
import pandas as pd
import joblib

st.title("Employee Attrition Prediction")
st.write("Enter employee details to predict whether the employee will leave the company.")

Age = st.number_input("Age", min_value=18, max_value=65)
MonthlyIncome = st.number_input("Monthly Income")
DistanceFromHome = st.number_input("Distance From Home")
YearsAtCompany = st.number_input("Years At Company")
JobSatisfaction = st.selectbox("Job Satisfaction", [1,2,3,4])
OverTime = st.selectbox("OverTime", ["Yes", "No"])

# Convert categorical valuepython -m streamlit --version
OverTime = 1 if OverTime == "Yes" else 0

user_input = pd.DataFrame({
    "Age":[Age],
    "MonthlyIncome":[MonthlyIncome],
    "DistanceFromHome":[DistanceFromHome],
    "YearsAtCompany":[YearsAtCompany],
    "JobSatisfaction":[JobSatisfaction],
    "OverTime":[OverTime]
})

model = joblib.load("employee_attrition_model.pkl")

if st.button("Predict"):
    prediction = model.predict(user_input)

    if prediction[0] == 1:
        st.error("Employee is likely to leave the company.")
    else:
        st.success("Employee is likely to stay in the company.")