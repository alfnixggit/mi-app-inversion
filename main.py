import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="InversionData Direct", page_icon="💰")
st.title("💰 Carga Directa (Intento 3)")

hoy = datetime.now().strftime('%d/%m/%Y')

# --- CONEXIÓN USANDO SECRETS ---
@st.cache_resource
def conectar():
    info = st.secrets["gcp_service_account"]
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    return gspread.authorize(creds)

try:
    gc = conectar()
    sh = gc.open("Inversiondata")
    
    ws_activos = sh.worksheet("APP1")
    activos = ws_activos.col_values(1)
    
    ws_log = sh.worksheet("LOG_MOV_PYTHON")
    data = ws_log.get_all_values()
    df_log = pd.DataFrame(data[1:], columns=data[0]) if len(data) > 1 else pd.DataFrame(columns=["FECHA", "ACTIVO", "VALOR"])

    datos_finales = {}
    for activo in activos:
        hist = df_log[df_log["ACTIVO"] == activo]
        ultimo_valor = hist.iloc[-1]["VALOR"] if not hist.empty else "0"
        
        ya_hecho = any((df_log["ACTIVO"] == activo) & (df_log["FECHA"] == hoy))
        
        c1, c2, c3 = st.columns([0.1, 0.5, 0.4])
        with c1: st.write("✅" if ya_hecho else "🔴")
        with c2: st.write(f"**{activo}**")
        with c3:
            val = st.text_input("Importe", value=ultimo_valor, key=activo, label_visibility="collapsed")
            datos_finales[activo] = val

    st.divider()
    if st.button("💾 GUARDAR JORNADA", use_container_width=True):
        filas_nuevas = [[hoy, a, v] for a, v in datos_finales.items()]
        ws_log.append_rows(filas_nuevas)
        st.success("¡Hecho!")
        st.cache_resource.clear()
        st.rerun()

except Exception as e:
    st.error(f"Error: {e}")
