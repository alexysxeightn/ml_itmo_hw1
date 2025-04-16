import streamlit as st 
import requests
from requests.exceptions import ConnectionError

ip_api = "model-api"
port_api = "5000"

# Заголовок приложения
st.title("Responce Prediction")

# Ввод данных
st.write("Enter details:")

gender = st.selectbox("Gender", ['Male', 'Female'])

age = st.text_input("Age", value=21)
if not age.isdigit():
    st.error("Please enter a valid number for Age.")

driving_license = st.selectbox("Driving License", [0, 1])

region_code = st.text_input("Region Code", value=35)
if not region_code.isdigit():
    st.error("Please enter a valid number for Region Code.")

previously_insured = st.selectbox("Previously Insured", [0, 1])

vehicle_age = st.selectbox("Vehicle Age", ['< 1 Year', '1-2 Year', '> 2 Years'])

vehicle_damage = st.selectbox("Vehicle Damage", ['Yes', 'No'])

annual_premium = st.text_input("Annual Premium", value=65101)
if not annual_premium.isdigit():
    st.error("Please enter a valid number for Annual Premium.")

policy_sales_channel = st.text_input("Policy Sales Channel", value=124)
if not policy_sales_channel.isdigit():
    st.error("Please enter a valid number for Policy Sales Channel.")

vintage = st.text_input("Vintage", value=187)
if not vintage.isdigit():
    st.error("Please enter a valid number for Vintage.")

# Кнопка для отправки запроса
if st.button("Predict"):
    # Проверка, что все поля заполнены
    if age.isdigit() and region_code.isdigit() and annual_premium.isdigit() and policy_sales_channel.isdigit() and vintage.isdigit():
        # Подготовка данных для отправки
        data = {
            "Gender": str(gender),
            "Age": int(age),
            "Driving_License": int(driving_license),
            "Region_Code": float(region_code),
            "Previously_Insured": int(previously_insured),
            "Vehicle_Age": str(vehicle_age),
            "Vehicle_Damage": str(vehicle_damage),
            "Annual_Premium": float(annual_premium),
            "Policy_Sales_Channel": float(policy_sales_channel),
            "Vintage": int(vintage),
        }

        try:
            # Отправка запроса к Flask API
            response = requests.post(f"http://{ip_api}:{port_api}/predict_model", json=data)

            # Проверка статуса ответа
            if response.status_code == 200:
                prediction = response.json()["prediction"]
                st.success(f"Prediction: {prediction}")
            else:
                st.error(f"Request failed with status code {response.status_code}")
        except ConnectionError as e:
            st.error(f"Failed to connect to the server")
    else:
        st.error("Please fill in all fields with valid numbers.")