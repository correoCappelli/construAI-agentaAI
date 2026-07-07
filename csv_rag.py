import pandas as pd
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_experimental.tools import PythonAstREPLTool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser

load_dotenv()

df = pd.read_csv("contenido/const_data.csv")
df["Payment Amount"] = pd.to_numeric(df["Payment Amount"], errors="coerce").fillna(0)
df["Total Project Value"] = pd.to_numeric(df["Total Project Value"], errors="coerce").fillna(0)
df["Balance Remaining"] = df["Total Project Value"] - df.groupby("Project ID")["Payment Amount"].cumsum()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

herramienta_py = PythonAstREPLTool(locals={"df": df})
llm_con_herramienta = llm.bind_tools([herramienta_py], tool_choice=herramienta_py.name)
parser = JsonOutputKeyToolsParser(key_name=herramienta_py.name, first_tool_only=True)

COLUMNS = [
    "Invoice Number","Client Name","Project ID","Payment Date","Payment Amount",
    "Payment Method","Description","Observation","Total Project Value","Balance Remaining"
]

system = f"""
Tienes acceso a un dataframe pandas `df` con las siguientes columnas exactas:
{COLUMNS}

Reglas:
- Usa SIEMPRE los nombres de columna tal cual aparecen arriba.
- Devuelve SIEMPRE dos partes:
  1. Un DataFrame, Series o gráfico con el resultado solicitado.
  2. Una explicación en lenguaje humano, breve y clara.
- NO muestres documentación ni metadata de objetos.
- Usa pandas, seaborn y matplotlib para cálculos y gráficos.
- Para balances, selecciona SIEMPRE el último registro ordenado por 'Payment Date'.
"""

prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{question}")])
cadena = prompt | llm_con_herramienta | parser | herramienta_py
