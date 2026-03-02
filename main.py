import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# Configuración visual para el iPhone
st.set_page_config(page_title="InversiónData", page_icon="📈")
st.title("📊 Mi Consola de Inversión")

# Conexión segura con Google Sheets
def conectar_google():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # Los secretos los configuraremos en el último paso en la web de la App
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    return gspread.authorize(creds)

try:
    cliente = conectar_google()
    sh = cliente.open("Inversiondata")
    
    # 1. Leer la lista de activos de la pestaña APP1
    ws_app1 = sh.worksheet("APP1")
    lista_activos = ws_app1.col_values(1)[1:] # Coge la columna A saltando el título

    # 2. Formulario de entrada
    st.subheader("Actualizar valores de hoy")
    fecha_hoy = datetime.now().strftime('%d/%m/%Y')
    st.write(f"📅 Fecha: **{fecha_hoy}**")

    datos_a_guardar = {}
    with st.form("formulario_inversion"):
        # Creamos un hueco para cada activo de tu lista
        for activo in lista_activos:
            datos_a_guardar[activo] = st.number_input(f"{activo} (€)", value=0.0, format="%.2f")
        
        enviar = st.form_submit_button("🚀 Grabar en LOG_MOV_PYTHON")

    # 3. Guardar en la pestaña seleccionada
    if enviar:
        ws_log = sh.worksheet("LOG_MOV_PYTHON")
        filas = []
        for activo, valor in datos_a_guardar.items():
            filas.append([fecha_hoy, activo, valor])
        
        ws_log.append_rows(filas)
        st.success("✅ ¡Datos guardados correctamente en Drive!")

except Exception as e:
    st.warning("🔄 Conectando con Google... Configura los 'Secrets' para activar la App.")
