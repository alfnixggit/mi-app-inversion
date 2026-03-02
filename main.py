import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# Configuración visual para el iPhone
st.set_page_config(page_title="InversiónData", page_icon="📈")
st.title("📊 Mi Consola de Inversión")

# Conexión segura con Google Sheets usando el ID directo
def conectar_google():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # Cargamos las credenciales desde los secrets de Streamlit
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    return gspread.authorize(creds)

try:
    cliente = conectar_google()
    
    # USAMOS EL ID DIRECTO PARA EVITAR ERRORES DE BÚSQUEDA
    # ID: 1x4bU3EVwmAEzUEmqPJ4gpMq402Mkxe2NylrJUBFBBWo
    sh = cliente.open_by_key("1x4bU3EVwmAEzUEmqPJ4gpMq402Mkxe2NylrJUBFBBWo")
    
    # 1. Leer la lista de activos de la pestaña APP1
    ws_app1 = sh.worksheet("APP1")
    lista_activos = ws_app1.col_values(1)[1:] # Coge la columna A saltando el título (Activo)

    # 2. Formulario de entrada
    st.subheader("Actualizar valores de hoy")
    fecha_hoy = datetime.now().strftime('%d/%m/%Y')
    st.write(f"📅 Fecha: **{fecha_hoy}**")

    datos_a_guardar = {}
    
    if not lista_activos:
        st.error("No se encontraron activos en la columna A de la pestaña APP1.")
    else:
        with st.form("formulario_inversion"):
            # Creamos un hueco para cada activo de tu lista
            for activo in lista_activos:
                if activo: # Solo si la celda no está vacía
                    datos_a_guardar[activo] = st.number_input(f"{activo} (€)", value=0.0, format="%.2f")
            
            enviar = st.form_submit_button("🚀 Grabar en LOG_MOV_PYTHON")

        # 3. Guardar en la pestaña seleccionada
        if enviar:
            try:
                ws_log = sh.worksheet("LOG_MOV_PYTHON")
                filas = []
                for activo, valor in datos_a_guardar.items():
                    filas.append([fecha_hoy, activo, valor])
                
                ws_log.append_rows(filas)
                st.success("✅ ¡Datos guardados correctamente en Drive!")
            except Exception as e_save:
                st.error(f"Error al guardar: ¿Existe la pestaña 'LOG_MOV_PYTHON'?")

except Exception as e:
    # Mostramos el error real para saber qué pasa si falla
    st.error(f"Error de conexión: {e}")
    st.warning("Revisa que los 'Secrets' en Streamlit tengan el formato correcto.")
