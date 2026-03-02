import streamlit as st
import gspread
from google.oauth2 import service_account

def conectar_con_filtro_total():
    try:
        s = dict(st.secrets["gcp_service_account"])
        pk_sucia = s["private_key"]

        # 1. Extraemos el texto entre los encabezados
        if "-----BEGIN PRIVATE KEY-----" in pk_sucia:
            cuerpo = pk_sucia.split("-----BEGIN PRIVATE KEY-----")[1].split("-----END PRIVATE KEY-----")[0]
        else:
            cuerpo = pk_sucia

        # 2. FILTRO RADICAL: Nos quedamos solo con caracteres válidos de Base64
        # Esto elimina tildes, espacios raros, guiones bajos invisibles, etc.
        caracteres_validos = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\n"
        cuerpo_limpio = "".join([c for c in cuerpo if c in caracteres_validos])

        # 3. Reconstrucción perfecta
        pk_final = f"-----BEGIN PRIVATE KEY-----\n{cuerpo_limpio.strip()}\n-----END PRIVATE KEY-----"
        s["private_key"] = pk_final

        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = service_account.Credentials.from_service_account_info(s, scopes=scopes)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error tras filtrado: {e}")
        return None

# --- APP ---
st.title("📊 Mi Panel de Inversión")

gc = conectar_con_filtro_total()

if gc:
    try:
        sh = gc.open("Inversiondata")
        st.success("✅ ¡POR FIN CONECTADO!")
        st.dataframe(sh.get_worksheet(0).get_all_records())
    except Exception as e:
        st.warning(f"La llave ya funciona, pero Google Sheets dice: {e}")
