import os
import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from pdf_rag import build_rag_pipeline, answer_question
from csv_rag import cadena

load_dotenv()
UPLOAD_DIR = "contenido"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("Gestor de Presupuestos de Construcción")

# --- PDF Upload Section ---
st.header("Carga de Presupuestos en PDF")

uploaded_files = st.file_uploader(
    "Sube uno o varios presupuestos en PDF",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    for i, uploaded_file in enumerate(uploaded_files):
        st.subheader(f"Datos para {uploaded_file.name}")

        client_name = st.text_input("Nombre del cliente", key=f"client_{i}")
        building_name = st.text_input("Nombre del edificio/obra", key=f"building_{i}")
        budget_number = st.number_input("Número de presupuesto", min_value=1, step=1, key=f"budget_{i}")

        if client_name and building_name and budget_number:
            safe_client = client_name.replace(" ", "_")
            safe_building = building_name.replace(" ", "_")
            filename = f"PRESUPUESTO{budget_number}_{safe_client}_{safe_building}.pdf"
            filepath = os.path.join(UPLOAD_DIR, filename)

            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"Presupuesto guardado como: {filename}")

# Botón para confirmar que ya terminaste
if st.button("Finalizar carga y construir índice"):
    st.session_state["rag_chain"] = build_rag_pipeline()
    st.success("Índice actualizado con los nuevos PDFs.")

# --- PDF Q&A ---
st.header("Preguntas sobre presupuestos")
user_question = st.text_input("Haz una pregunta sobre los presupuestos")

if user_question:
    if "rag_chain" not in st.session_state:
        st.warning("Primero debes finalizar la carga de PDFs y construir el índice.")
    else:
        respuesta = answer_question(st.session_state["rag_chain"], user_question)
        if respuesta:
            st.write("### Respuesta")
            st.write(respuesta)
        else:
            st.error("No se obtuvo respuesta del modelo. Verifica que los PDFs tengan contenido válido.")

# --- CSV Accounting Section ---
st.header("Consultas de Contabilidad (CSV)")

csv_question = st.text_input("Pregunta sobre facturas, pagos y balances")

if csv_question:
    try:
        resultado = cadena.invoke({"question": csv_question})
        st.write("### Respuesta Contable")

        if isinstance(resultado, pd.DataFrame):
            st.table(resultado if not resultado.empty else pd.DataFrame({"Aviso": ["No se encontraron registros."]}))
        elif isinstance(resultado, pd.Series):
            st.table(resultado.to_frame())
        elif isinstance(resultado, (float, int, np.floating)):
            st.write(f"Resultado numérico: {float(resultado):.2f}")
        elif isinstance(resultado, str):
            if "DataFrame" in resultado and "Parameters" in resultado:
                st.warning("El modelo devolvió documentación en lugar de datos.")
            else:
                st.write(resultado)
        else:
            st.write(resultado)

        if plt.get_fignums():
            st.pyplot(plt.gcf())
            plt.close()

    except Exception as e:
        st.error(f"Error al procesar la pregunta: {e}")
