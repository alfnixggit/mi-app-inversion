import streamlit as st
import gspread
from google.oauth2 import service_account
import re

def conectar_definitivo():
    try:
        # Obtenemos los datos del cuadro de Secrets
        s = dict(st.secrets["gcp_service_account"])
        pk = s["private_key"]

        # --- LIMPIEZA QUIRÚRGICA ---
        # 1. Si la llave tiene \n escrito como texto, lo convertimos a salto real
        pk = pk.replace("\\n", "\n")
        
        # 2. Extraemos solo lo que hay entre los guiones de BEGIN y END
        # Esto elimina cualquier carácter extraño (como el guion bajo del error) que esté fuera
        if "-----BEGIN PRIVATE KEY-----" in pk:
            cuerpo = pk.split("-----BEGIN PRIVATE KEY-----")[1].split("-----END PRIVATE KEY-----")[0]
            # Limpiamos espacios y saltos de línea vacíos del cuerpo
            cuerpo = cuerpo.strip()
            # Reconstruimos la llave perfecta
            pk_limpia = f"-----BEGIN PRIVATE KEY-----\n{cuerpo}\n-----END PRIVATE KEY-----"
        else:
            pk_limpia = pk.strip()

        s["private_key"] = pk_limpia

        # Configuración de permisos
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = service_account.Credentials.from_service_account_info(s, scopes=scopes)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error en el formato de la llave: {e}")
        return None

# --- APP ---
st.title("📊 Mi Panel de Inversión")

gc = conectar_definitivo()

if gc:
    try:
        # Abrimos tu archivo (asegúrate que el nombre sea exacto)
        sh = gc.open("Inversiondata")
        st.success("✅ ¡CONECTADO!")
        st.dataframe(sh.get_worksheet(0).get_all_records())
    except Exception as e:
        st.warning(f"Llave aceptada, pero no accedo al archivo: {e}")
        st.info("Asegúrate de haber invitado a: python-app@careful-broker-395321.iam.gserviceaccount.com")
