import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

FASTAPI_URL = "https://8f02-34-41-88-204.ngrok-free.app/predict"  # Replace

st.title("Energy Consumption Forecast")

sector = st.selectbox("Select Sector", ["Commercial", "Industrial"])
months = st.selectbox("Forecast Period (months)", [3, 6, 9, 12])

if st.button("Predict"):
    with st.spinner("Fetching forecast..."):
        try:
            response = requests.get(FASTAPI_URL, params={"sector": sector, "months": months})
            result = response.json()
            st.write("API Response:", result)


            df = pd.DataFrame({
                "Date": result["dates"],
                "Forecast": result["forecast"],
                "Lower_CI": result["lower"],
                "Upper_CI": result["upper"]
            })

            st.success("Forecast fetched!")
            st.dataframe(df)
            # Plot
            # recent_actual = extended_series.dropna().iloc[-9:].round().astype(int)   
            fig = go.Figure()    
            # fig.add_trace(go.Scatter(x=recent_actual.index, y=recent_actual, mode='lines+markers', name='Last 12 Months Actual'))
            fig.add_trace(go.Scatter(x=forecast.index, y=forecast, mode='lines+markers', name='Forecast'))
            fig.add_trace(go.Scatter(x=forecast.index, y=Lower_CI, mode='lines', name='Lower CI', line=dict(dash='dot')))
            fig.add_trace(go.Scatter(x=forecast.index, y=Upper_CI, mode='lines', name='Upper CI', line=dict(dash='dot')))
            fig.update_layout(title="Forecast from Current Month Onward", xaxis_title="Date", yaxis_title="Consumption")
            st.plotly_chart(fig)
            # st.line_chart(df.set_index("Date")[["Forecast", "Lower CI", "Upper CI"]])

        except Exception as e:
            response = requests.get(FASTAPI_URL, params={"sector": sector, "months": months})
            # result = response.json()
            st.write("API Response:", response)
            st.error(f"Something went wrong: {e}")
