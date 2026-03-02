import streamlit as st
import gspread
from google.oauth2 import service_account

def conectar_blindado():
    try:
        # Extraemos los datos del secreto
        s = dict(st.secrets["gcp_service_account"])
        
        # --- PROCESO DE LIMPIEZA TOTAL ---
        pk = s["private_key"]
        
        # 1. Quitamos espacios en blanco, puntos o comas accidentales al inicio/final
        pk = pk.strip().strip('.').strip(',')
        
        # 2. Corregimos los saltos de línea (por si se pegaron como \n)
        pk = pk.replace("\\n", "\n")
        
        # 3. Nos aseguramos de que no haya espacios al inicio de cada línea interna
        lineas = [linea.strip() for linea in pk.split('\n') if linea.strip()]
        pk_limpia = "\n".join(lineas)
        
        # Guardamos la llave limpia
        s["private_key"] = pk_limpia

        # Configuración de Google
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = service_account.Credentials.from_service_account_info(s, scopes=scopes)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error detectado en la llave: {e}")
        return None

# --- INTERFAZ ---
st.title("📊 Mi Panel de Inversión")

gc = conectar_blindado()

if gc:
    try:
        # Conectamos con tu archivo "Inversiondata"
        sh = gc.open("Inversiondata")
        hoja = sh.get_worksheet(0)
        st.success("✅ ¡Conectado correctamente!")
        st.dataframe(hoja.get_all_records())
    except Exception as e:
        st.warning(f"Llave aceptada, pero hay un problema con el Excel: {e}")
        st.info("Asegúrate de haber compartido el Excel con: python-app@careful-broker-395321.iam.gserviceaccount.com")
