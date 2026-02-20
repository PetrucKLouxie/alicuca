import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Analisis Dataset", layout="wide")

st.title("📊 Dashboard Analisis Dataset")

@st.cache_data
def load_data():
    try:
        return pd.read_csv("dataset.csv", encoding="utf-8")
    except:
        try:
            return pd.read_csv("dataset.csv", encoding="latin1")
        except:
            return pd.read_csv("dataset.csv", sep=";")

# Load dataset
try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal membaca dataset: {e}")
    st.stop()

# Jika berhasil lanjut
st.subheader("Preview Dataset")
st.dataframe(df)

st.subheader("Informasi Dataset")
col1, col2, col3 = st.columns(3)
col1.metric("Jumlah Baris", df.shape[0])
col2.metric("Jumlah Kolom", df.shape[1])
col3.metric("Missing Values", df.isnull().sum().sum())

numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

if numeric_columns:
    st.subheader("Visualisasi Data")
    selected_column = st.selectbox("Pilih kolom numerik", numeric_columns)

    fig = px.histogram(df, x=selected_column, title=f"Distribusi {selected_column}")
    st.plotly_chart(fig, use_container_width=True)

    fig_box = px.box(df, y=selected_column, title=f"Boxplot {selected_column}")
    st.plotly_chart(fig_box, use_container_width=True)
else:
    st.warning("Tidak ada kolom numerik untuk divisualisasikan.")

st.subheader("Statistik Deskriptif")
st.write(df.describe())
