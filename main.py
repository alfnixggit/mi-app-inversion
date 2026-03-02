import streamlit as st
import gspread
from google.oauth2 import service_account

def conectar_sin_errores():
    try:
        s = dict(st.secrets["gcp_service_account"])
        pk = s["private_key"].replace("\\n", "\n")
        
        # Limpieza de encabezados
        if "-----BEGIN PRIVATE KEY-----" in pk:
            cuerpo = pk.split("-----BEGIN PRIVATE KEY-----")[1].split("-----END PRIVATE KEY-----")[0]
        else:
            cuerpo = pk

        # Filtro de caracteres y REPARACIÓN DE PADDING
        cuerpo = "".join(c.strip() for c in cuerpo if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=")
        
        # Forzar que el largo sea múltiplo de 4 (Arregla el InvalidPadding)
        while len(cuerpo) % 4 != 0:
            cuerpo += "="

        pk_final = f"-----BEGIN PRIVATE KEY-----\n{cuerpo}\n-----END PRIVATE KEY-----"
        s["private_key"] = pk_final

        creds = service_account.Credentials.from_service_account_info(
            s, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        )
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error: {e}")
        return None

st.title("📊 Panel de Inversión")
gc = conectar_sin_errores()
if gc:
    try:
        sh = gc.open("Inversiondata")
        st.success("¡POR FIN!")
        st.dataframe(sh.get_worksheet(0).get_all_records())
    except Exception as e:
        st.info(f"Conexión OK. Error de acceso al archivo: {e}")
