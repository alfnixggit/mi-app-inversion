import streamlit as st
import pandas as pd

st.title("📊 Mi Panel de Inversión")

# PEGA AQUÍ LA URL DE TU EXCEL
URL_EXCEL = "TU_URL_AQUÍ"

# Esta pequeña función convierte la URL normal en una de descarga directa
def conseguir_url_csv(url):
    try:
        id_archivo = url.split("/")[-2]
        return f"https://docs.google.com/spreadsheets/d/{id_archivo}/export?format=csv"
    except:
        return None

if URL_EXCEL != "TU_URL_AQUÍ":
    url_final = conseguir_url_csv(URL_EXCEL)
    try:
        df = pd.read_csv(url_final)
        st.success("✅ ¡CONECTADO AL INSTANTE!")
        st.dataframe(df)
    except Exception as e:
        st.error(f"No pude leer el Excel. Revisa que sea público: {e}")
else:
    st.info("Por favor, pega la URL de tu Google Sheet en el código.")
