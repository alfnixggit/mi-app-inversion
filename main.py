import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. TUS DIRECCIONES (No cambian)
URL_LOG = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT_BWK0W-ckq-8381mddbvScIyjaGyhsRUBBZhckjEmXZTjmCX-DE5rztmylPv6KAVJQVkhH3k9-YCm/pub?gid=1403494531&single=true&output=csv"
URL_APP1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT_BWK0W-ckq-8381mddbvScIyjaGyhsRUBBZhckjEmXZTjmCX-DE5rztmylPv6KAVJQVkhH3k9-YCm/pub?gid=153180669&single=true&output=csv"
BASE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfnR3UDEnLAg1hqNfS4vApGfAR3e-wT_WyMDMS_Xqg9rc0C-Q/viewform"

st.set_page_config(page_title="InversionData", page_icon="💰")
st.title("💰 Captación de Datos")

hoy = datetime.now().strftime('%d/%m/%Y')
st.info(f"Fecha de hoy: {hoy}")

# 2. CARGA DE DATOS
try:
    df_v = pd.read_csv(URL_APP1)
    df_l = pd.read_csv(URL_LOG)
except:
    st.error("Error cargando el Excel. Revisa la conexión.")
    st.stop()

# 3. INTERFAZ DE CARGA RÁPIDA
st.subheader("Introduce los valores de hoy:")

for activo in df_v.iloc[:, 0]:
    # Comprobar si ya se ha grabado hoy
    ya_grabado = any((df_l.iloc[:, 1] == activo) & (df_l.iloc[:, 0].str.contains(hoy)))
    
    col1, col2, col3 = st.columns([0.1, 0.5, 0.4])
    
    with col1:
        st.write("🟢" if ya_grabado else "🔴")
    
    with col2:
        st.write(f"**{activo}**")
        
    with col3:
        # Aquí metes el número
        valor = st.text_input("Importe", key=activo, label_visibility="collapsed", placeholder="0.00")
        
        if valor:
            # Generamos el enlace pre-rellenado automáticamente
            params = {
                "entry.1843422617": activo, # Código interno del campo Activo
                "entry.845943568": valor    # Código interno del campo Valor
            }
            url_rellena = f"{BASE_FORM_URL}?usp=pp_url&{urllib.parse.urlencode(params)}"
            
            st.markdown(f'''
                <a href="{url_rellena}" target="_blank" style="text-decoration:none;">
                    <div style="background-color:#28a745;color:white;padding:5px;text-align:center;border-radius:5px;font-size:12px;font-weight:bold;">
                        ENVIAR {activo}
                    </div>
                </a>
            ''', unsafe_allow_html=True)

st.divider()
if st.button("🔄 Actualizar Semáforo"):
    st.rerun()
