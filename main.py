import streamlit as st
import pandas as pd
from datetime import datetime

# 1. DIRECCIONES DE TUS DATOS
URL_LOG = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT_BWK0W-ckq-8381mddbvScIyjaGyhsRUBBZhckjEmXZTjmCX-DE5rztmylPv6KAVJQVkhH3k9-YCm/pub?gid=1403494531&single=true&output=csv"
URL_APP1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT_BWK0W-ckq-8381mddbvScIyjaGyhsRUBBZhckjEmXZTjmCX-DE5rztmylPv6KAVJQVkhH3k9-YCm/pub?gid=153180669&single=true&output=csv"
URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSfnR3UDEnLAg1hqNfS4vApGfAR3e-wT_WyMDMS_Xqg9rc0C-Q/viewform"

st.title("💰 InversionData")
hoy = datetime.now().strftime('%d/%m/%Y')

# 2. LEER EXCEL
df_v = pd.read_csv(URL_APP1)
try:
    df_l = pd.read_csv(URL_LOG)
except:
    df_l = pd.DataFrame(columns=['Marca temporal', 'Activo', 'Valor'])

# 3. DIBUJAR SEMÁFORO
st.subheader(f"Estado de hoy: {hoy}")

for activo in df_v.iloc[:, 0]:
    actualizado = False
    if not df_l.empty:
        # Busca el nombre del activo y si la fecha de hoy está en la marca temporal
        actualizado = any((df_l.iloc[:, 1] == activo) & (df_l.iloc[:, 0].str.contains(hoy)))
    
    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        st.write("🟢" if actualizado else "🔴")
    with col2:
        st.write(activo)

st.divider()

# 4. BOTÓN PARA EL MÓVIL
st.markdown(f"""
    <a href="{URL_FORM}" target="_blank" style="text-decoration:none;">
        <div style="background-color:#28a745;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:20px;">
            ➕ INTRODUCIR DATO
        </div>
    </a>
    """, unsafe_allow_html=True)

if st.button("🔄 Refrescar"):
    st.rerun()
