import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# --- LA LLAVE MAESTRA REFORMATEADA ---
INFO_LLAVE = {
  "type": "service_account",
  "project_id": "careful-broker-395321",
  "private_key_id": "75c0576acd9256ef5c04419f9e4a6df4d7a8c2e8",
  "private_key": st.secrets.get("private_key", "").replace("\\n", "\n") if "private_key" in st.secrets else "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDalENj9EncBiy9\nFly88YllR+2qMjrNbw7+vnde/I6TyFj1frmUXSWZeRXLv8TJbDxcIcOBoU8+TKcd\nQFbfnCSKdj6b6R+3zBi/+WboWcwYymvVHEm5avPvGfZLJktaZvfdy3ykZ2rDWa6l\nzFLTcjI24/wMuL1w/KowXF6Ji0xtyW6ohNBWy4BFMsILI5MaDqt6nT5FXkC6diG+\nkQ68lTCIFk8+aBVy8vEXQJuvq29KMst3qqYGtuIgZXkzwErnPqjyR9TXzVw06OYi\nRelcPjoqPsdP9rppMKBR11c0AKHnNb0yQKjWHZBawxGiFjySMdqpbEnN5qB7gy9V\nI05TOJ13AgMBAAECggEAWqF7R+i071xIFKc/EMD9/VbTvuxQ4XmZOBt1l5cU70X1\nTOWcwV3WB0rjtLXxPKt6Y6FEVW2zU9uot0JEQzeVFyxsTW1eT3F7Ga6p8tG5BNZ5\n28V89DrapluXehWIzRVA1WBYcDrJU/LNrcWI2k/Rbl0d15CKTF0XnDHQqStvJ13I\nFAdvDE3NtlXcMDyr0HKRPt8ZsLyicVWZMIp/Ajp7PwA2mmqgKSP1HiX53MxcX7+n\nHfwbOSUG5M2avsQjuVblE92I1rho33C5kRxugNzyIE28tLQJ1IMdW7hW6efNw0IS\nesxLDnoX28byvYasIh9hwBYmJz6sRxZamkP5thSdsQKBgQD0fukuOkVGztRBc1oE\n7IKoR+Xn/i4RZl+sZd9qMBt5PI+FRsrp7OE2R8PNegN0tGaLZ7D7q14GrDl1AuRW\nq3zKafryhL93N2ph4lcDMgXLQEdFqQh5FUp2wa0+2MHcypQ1qyZ5JE2Qb0Dv5BkA\nBKLOtEQzbp38eT81/XIeqrskewKBgQDk3SwjQPmEBFzu/A3MiGqD300o3xrAPTHj\nAL6cKEy/BmIW31pyWewjb8MfPWEMWghAnLqXaMdczXURvAO0f1YJA0+cBjTrTbTY\nmtf4+bVrMLynoeltPf8NodJhve4wFYd+LJSLbUGSxaq6/qitzU3k1Cp/MYKGwAzn\nMTspuPkwNQKBgC+4AVzTZKgAQC8SC3TAkHO1rKqN0oH04CFutJ8uCn6sEjrp6Tqk\n0APfF9knwjrp5sW4lDNaa/yTapdq3BQKXk3HR4JD5HapKys1mNP31GeqAP8YkZ3I\nSQNKo7yLY7LrGugqolSsgDL7c8oeU77MKNZ9Gn6LTWx0YaDw+XAA1Iu3AoGBAJAZ\ciEAWBp3ZMxUh5uwiOBfSQXi88T2wuJbJajM9wWPz1L3bstxMu1dAU46J1DPn0KP\nbCzJHD2iX4O7DdooEtO58fYbMla1pph7ZmCtWT0UgrRJjd/qmRzMNtqz67T62UTo\nbN8c+5yeONFkZnCIQ/NAY0GSusx9P6KRrN6oSL3BAoGAfL+YS5AWhmS9s0Xfeoo\n4vdah7Xq5gBuzgEGbDnTS+vObqrbbIjXsPZp6m+/pRWZ4Ct6yc87+j6tMhRCxE0e\nYb2UL6hIxzuBRv56xEzD1bJ10H4o2zLN8kKVqUIxVQhBpcPOA+lZhzG6DGrRn5IU\nE2UzrKE0vK+KW0Ny+rzxiq0=\n-----END PRIVATE KEY-----\n",
  "client_email": "python-app@careful-broker-395321.iam.gserviceaccount.com",
  "client_id": "108343647994793129429",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/python-app%40careful-broker-395321.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# --- LÓGICA ---
st.set_page_config(page_title="InversionData Direct", page_icon="⚡")
st.title("⚡ Carga Directa (Sin Formularios)")

hoy = datetime.now().strftime('%d/%m/%Y')

try:
    # Conexión limpia
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    # Corregimos manualmente los saltos de línea de la llave si vienen mal
    INFO_LLAVE["private_key"] = INFO_LLAVE["private_key"].replace("\\n", "\n")
    
    creds = Credentials.from_service_account_info(INFO_LLAVE, scopes=SCOPES)
    client = gspread.authorize(creds)
    sh = client.open("Inversiondata")
    
    ws_activos = sh.worksheet("APP1")
    activos = ws_activos.col_values(1)
    
    ws_log = sh.worksheet("LOG_MOV_PYTHON")
    data_log = ws_log.get_all_values()
    df_log = pd.DataFrame(data_log[1:], columns=data_log[0]) if len(data_log) > 1 else pd.DataFrame(columns=["FECHA", "ACTIVO", "VALOR"])
except Exception as e:
    st.error(f"Error técnico: {e}")
    st.stop()

datos_a_guardar = {}
for activo in activos:
    df_activo = df_log[df_log["ACTIVO"] == activo]
    ultimo_val = df_activo.iloc[-1]["VALOR"] if not df_activo.empty else "0"
    
    ya_existe = any((df_log["ACTIVO"] == activo) & (df_log["FECHA"] == hoy))
    
    col1, col2, col3 = st.columns([0.1, 0.5, 0.4])
    with col1: st.write("✅" if ya_existe else "⚪")
    with col2: st.write(f"**{activo}**")
    with col3:
        valor = st.text_input("Importe", value=ultimo_val, key=activo, label_visibility="collapsed")
        datos_a_guardar[activo] = valor

if st.button("💾 GUARDAR TODO EN EL EXCEL", use_container_width=True):
    nuevas_filas = [[hoy, act, val] for act, val in datos_a_guardar.items()]
    try:
        ws_log.append_rows(nuevas_filas)
        st.success("¡Datos guardados!")
        st.rerun()
    except Exception as e:
        st.error(f"Error al guardar: {e}")
