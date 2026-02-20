import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Trend Analisis Cuaca", layout="wide")

st.title("🌦️ Trend Analisis Cuaca")

# Upload file
uploaded_file = st.file_uploader("Upload Dataset Cuaca (CSV)", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Ubah kolom tanggal jadi datetime
        df['time (UTC)'] = pd.to_datetime(df['date'])

        st.success("Dataset berhasil dimuat ✅")

        # Sort berdasarkan tanggal
        df = df.sort_values('date')

        st.subheader("Preview Data")
        st.dataframe(df.head())

        # =========================
        # 📈 Trend Line Chart
        # =========================
        st.subheader("📈 Trend Cuaca Harian")

        weather_columns = df.select_dtypes(include=['int64','float64']).columns.tolist()

        selected_metric = st.selectbox(
            "Pilih Parameter Cuaca",
            weather_columns
        )

        fig = px.line(
            df,
            x="date",
            y=selected_metric,
            title=f"Trend {selected_metric} terhadap Waktu",
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)

        # =========================
        # 📊 Moving Average
        # =========================
        st.subheader("📊 Moving Average (Rata-rata Bergerak)")

        window = st.slider("Pilih Window (hari)", 3, 30, 7)

        df[f"{selected_metric}_MA"] = df[selected_metric].rolling(window=window).mean()

        fig_ma = px.line(
            df,
            x="date",
            y=[selected_metric, f"{selected_metric}_MA"],
            title=f"Trend & Moving Average ({window} Hari)"
        )

        st.plotly_chart(fig_ma, use_container_width=True)

        # =========================
        # 🌧️ Total Curah Hujan
        # =========================
        if "rainfall" in df.columns:
            st.subheader("🌧️ Total Curah Hujan")

            total_rain = df["rainfall"].sum()
            avg_rain = df["rainfall"].mean()

            col1, col2 = st.columns(2)
            col1.metric("Total Curah Hujan", f"{total_rain:.2f}")
            col2.metric("Rata-rata Harian", f"{avg_rain:.2f}")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

else:
    st.info("Silakan upload dataset CSV untuk memulai analisis.")
