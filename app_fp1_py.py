import streamlit as st
import pandas as pd
import requests
from datetime import datetime

FASTAPI_URL = "https://8f02-34-41-88-204.ngrok-free.app/predict"  # Replace

st.title("⚡Electricity Generation Forecast")

sector = st.selectbox("Select Sector", ["Commercial", "Industrial"])
months = st.selectbox("Forecast Period (months)", [3, 6])

if st.button("Forecast"):
    with st.spinner("Fetching forecast..."):
        try:
            response = requests.get(FASTAPI_URL, params={"sector": sector, "months": months})
            result = response.json()
            # st.write("API Response:", result)


            df = pd.DataFrame({
                "Date": result["dates"],
                "Forecast": result["forecast"],
                "Lower CI": result["lower"],
                "Upper CI": result["upper"]
            })
            df["Date"] = pd.to_datetime(df["Date"]).dt.date

            st.success("Forecast fetched!")
            st.dataframe(df)
            st.success("Forecast of electricity generation from current month in million kilowatthour")
            st.line_chart(df.set_index("Date")[["Forecast", "Lower CI", "Upper CI"]])

        except Exception as e:
            response = requests.get(FASTAPI_URL, params={"sector": sector, "months": months})
            # result = response.json()
            st.write("API Response:", response)
            st.error(f"Something went wrong: {e}")
