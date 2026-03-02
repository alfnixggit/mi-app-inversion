import streamlit as st
import gspread
from google.oauth2 import service_account

# --- CONFIGURACIÓN DE LAS CREDENCIALES ---

def conseguir_cliente_google():
    # 1. Leemos los secretos que pegaste en Streamlit Cloud
    try:
        creds_dict = st.secrets["gcp_service_account"]
    except KeyError:
        st.error("No se encontró la sección [gcp_service_account] en los Secrets de Streamlit.")
        return None

    # 2. LIMPIADORA: Corregimos problemas comunes de formato en la llave privada
    if "private_key" in creds_dict:
        # Esto arregla el error de "Invalid data" o problemas con el signo =
        creds_dict_copy = dict(creds_dict)
        creds_dict_copy["private_key"] = creds_dict_copy["private_key"].replace("\\n", "\n")
    else:
        st.error("La llave 'private_key' no está dentro de tus secretos.")
        return None

    # 3. Creamos el objeto de credenciales oficial de Google
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    credenciales = service_account.Credentials.from_service_account_info(
        creds_dict_copy, 
        scopes=scopes
    )
    
    # 4. Autorizamos la conexión
    return gspread.authorize(credenciales)

# --- INICIO DE LA APLICACIÓN ---

st.title("Mi App de Inversión")

# Intentamos conectar
gc = conseguir_cliente_google()

if gc:
    st.success("¡Conexión establecida con éxito!")
    
    # IMPORTANTE: Cambia "Nombre de tu Excel" por el nombre real de tu archivo
    # Y recuerda compartir el Excel con el email de la cuenta de servicio
    try:
        # Ejemplo: sh = gc.open("Tu Hoja de Google")
        # st.write("Conectado a la hoja correctamente")
        pass
    except Exception as e:
        st.info("Conexión técnica lista. Ahora asegúrate de haber compartido tu Excel con el email de la Service Account.")
