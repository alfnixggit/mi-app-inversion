import streamlit as st
import pandas as pd
from datetime import datetime

CONFIGURACIÓN
URL_LOG = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT_BWK0W-ckq-8381mddbvScIyjaGyhsRUBBZhckjEmXZTjmCX-DE5rztmylPv6KAVJQVkhH3k9-YCm/pub?gid=1403494531&single=true&output=csv"
URL_APP1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT_BWK0W-ckq-8381mddbvScIyjaGyhsRUBBZhckjEmXZTjmCX-DE5rztmylPv6KAVJQVkhH3k9-YCm/pub?gid=153180669&single=true&output=csv"
URL_FORMULARIO = "https://docs.google.com/forms/d/e/1FAIpQLSfnR3UDEnLAg1hqNfS4vApGfAR3e-wT_WyMDMS_Xqg9rc0C-Q/viewform"

st.set_page_config(page_title="InversionData Pro", page_icon="📈")

@st.cache_data(ttl=10)
def cargar_datos():
df_v = pd.read_csv(URL_APP1)
try:
df_l = pd.read_csv(URL_LOG)
except:
df_l = pd.DataFrame(columns=['Marca temporal', 'Activo', 'Valor'])
return df_v, df_l

df_vars, df_log = cargar_datos()
hoy = datetime.now().strftime('%d/%m/%Y')

st.title("💰 Mi Consola Financiera")
st.info(f"Fecha de hoy: {hoy}")

st.subheader("Estado de Carga")
for activo in df_vars.iloc[:, 0]:
actualizado = False
if not df_log.empty:
actualizado = any((df_log.iloc[:, 1] == activo) & (df_log.iloc[:, 0].str.contains(hoy)))
col1, col2 = st.columns([0.2, 0.8])
with col1:
st.write("🟢" if actualizado else "🔴")
with col2:
st.write(f"{activo}")

st.divider()

st.markdown(f'<a href="{URL_FORMULARIO}" target="_blank" style="text-decoration:none;"><div style="background-color:#28a745;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:20px;">➕ INTRODUCIR DATOS</div></a>', unsafe_allow_html=True)

if st.button("🔄 Refrescar Semáforo"):
st.rerun()
