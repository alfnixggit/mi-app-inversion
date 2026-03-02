import streamlit as st
import gspread
from google.oauth2 import service_account

def conectar_seguro():
    try:
        s = st.secrets["gcp_service_account"]
        
        # Limpieza extrema de la llave
        llave = s["private_key"]
        # 1. Quitamos comillas si se colaron
        llave = llave.strip("'").strip('"')
        # 2. Convertimos los \n de texto en saltos de línea reales
        llave = llave.replace("\\n", "\n")
        # 3. Quitamos espacios vacíos al inicio y final
        llave = llave.strip()

        info = {
            "type": "service_account",
            "project_id": s["project_id"],
            "private_key_id": s["private_key_id"],
            "private_key": llave,
            "client_email": s["client_email"],
            "token_uri": s["token_uri"],
        }

        creds = service_account.Credentials.from_service_account_info(
            info, 
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        )
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error al procesar la llave: {e}")
        return None

st.title("Mi App de Inversión")

gc = conectar_seguro()

if gc:
    try:
        # Usamos el nombre que vi en tu foto
        sh = gc.open("Inversiondata")
        st.success("¡CONECTADO CON ÉXITO!")
        st.dataframe(sh.get_worksheet(0).get_all_records())
    except Exception as e:
        st.warning(f"Conectado a Google, pero no encuentro el Excel: {e}")
