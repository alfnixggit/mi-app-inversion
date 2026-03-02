import streamlit as st
import gspread
from google.oauth2 import service_account

# Esto es lo que lee el cuadro de "Secrets" que configuramos antes
# y soluciona el error del signo '=' de la llave
creds_dict = st.secrets["gcp_service_account"]
credentials = service_account.Credentials.from_service_account_info(creds_dict)

# Aquí le damos permisos para entrar a Google Drive y Sheets
scoped_credentials = credentials.with_scopes([
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
])

# Conexión final
gc = gspread.authorize(scoped_credentials)

# Prueba a abrir tu archivo (cambia 'Mi Hoja de Inversión' por el nombre real de tu Excel)
# sh = gc.open("Mi Hoja de Inversión")
# st.success("¡Conexión exitosa!")
