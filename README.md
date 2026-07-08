# 📊 REACT Agent con LangChain, Chroma y OpenAI

Este proyecto es una aplicación desplegada en **Streamlit** que implementa un agente **RAG (Retrieval-Augmented Generation)** con capacidades avanzadas de procesamiento de PDFs y CSVs. Está potenciado por **LangChain**, **ChromaDB**, técnicas de **Semantic Chunking** y modelos de lenguaje de **OpenAI**.

---

## 🚀 Funcionalidades principales

- **[Carga de presupuestos en PDF](ca://s?q=Cargar_presupuestos_en_PDF)**  
  Permite subir múltiples presupuestos en formato PDF.  
  Cada archivo se renombra automáticamente con los campos ingresados: **Cliente**, **Edificio** y **Número de Presupuesto**.

- **[Consulta de datos en CSV](ca://s?q=Consulta_de_datos_en_CSV)**  
  Se pueden subir archivos CSV con información de facturas y pagos.  
  El agente responde preguntas sobre los datos, como montos pendientes, pagos realizados o estadísticas de facturación.

- **[Pipeline RAG](ca://s?q=Pipeline_RAG)**  
  Integración con **ChromaDB** y **Semantic Chunking** para mejorar la recuperación de información desde documentos PDF.

- **[Interfaz interactiva](ca://s?q=Interfaz_en_Streamlit)**  
  Construida en **Streamlit**, con una experiencia simple y clara para cargar archivos, hacer consultas y visualizar resultados.

---

## 🛠️ Tecnologías utilizadas

- [Streamlit](ca://s?q=Streamlit) `1.36.0`  
- [LangChain](ca://s?q=LangChain) + [LangChain-OpenAI](ca://s?q=LangChain_OpenAI) + [LangChain-Community](ca://s?q=LangChain_Community)  
- [ChromaDB](ca://s?q=ChromaDB)  
- [Semantic Chunking](ca://s?q=Semantic_Chunking) con `langchain-experimental`  
- [OpenAI LLM](ca://s?q=OpenAI_LLM)  
- [Pandas](ca://s?q=Pandas) y [NumPy](ca://s?q=NumPy) para cálculos sobre CSVs  
- [Matplotlib](ca://s?q=Matplotlib) para visualizaciones

---

## 📂 Estructura del proyecto

```plaintext
├── app.py                # Aplicación principal en Streamlit
├── pdf_rag.py            # Pipeline RAG para PDFs
├── csv_rag.py            # Procesamiento y consultas sobre CSV
├── contenido/const_data.csv   # archivo CSV con los datos de facturacion
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Este archivo


## 📑 Ejemplo de archivo CSV

El proyecto incluye un archivo de ejemplo en la carpeta `contenido/` llamado **const_data.csv**.  
Este archivo contiene información de facturas y pagos, con la siguiente estructura:

```csv
Invoice Number,Client Name,Project ID,Payment Date,Payment Amount,Payment Method,Description,Observation,Total Project Value,Balance Remaining
INV-2026-001,Martinez & Sons,PRJ-2026-07,2026-07-02,1500.00,Bank Transfer,Foundation work,Client requested early delivery,5000.00,3500.00
INV-2026-002,Gomez Builders,PRJ-2026-08,2026-07-05,2000.00,Cash,Roof installation,Payment delayed by 2 days,8000.00,6000.00
INV-2026-003,Rivera Construction,PRJ-2026-09,2026-07-10,2500.00,Check,Interior finishing,Discount applied for bulk materials,10000.00,7500.00
INV-2026-004,López Renovations,PRJ-2026-10,2026-07-12,1200.00,Bank Transfer,Painting,Client asked for color change,4000.00,2800.00
INV-2026-005,Perez & Co,PRJ-2026-11,2026-07-15,3000.00,Credit Card,Electrical wiring,Inspection scheduled next week,7000.00,4000.00
FAC-001,FAMCA,PRESUPUESTO 1,2026-07-15,3000.00,Credit Card,Electrical wiring,ventanas newbery,7000.00,4000.00


## ⚠️ Importante sobre los nombres de las columnas

- Los nombres de las columnas **deben mantenerse tal cual** para que el agente pueda interpretar correctamente los datos.  
- Si decides cambiarlos (por ejemplo, simplificarlos a `invoice`, `client`, `project`, etc.), deberás modificar también las partes del código que hacen referencia a esas columnas.

---

## 🐍 Ejemplo de renombrado en pandas

```python
import pandas as pd

df = pd.read_csv("contenido/const_data.csv")

df.columns = [
    "invoice", "client", "project", "date", "amount",
    "method", "description", "observation", "total_value", "balance"
]


## 🔧 Ajustes necesarios en el código

- En **csv_rag.py**: cualquier acceso a columnas (ejemplo: `df["Client Name"]`) debe actualizarse al nuevo nombre (`df["client"]`).  
- En los **prompts de LangChain**: si se hace referencia a los nombres originales de las columnas, también deben actualizarse.  
- En las funciones de **pandas** o cálculos (`groupby`, `filter`, etc.), asegúrate de usar los nombres nuevos.


---

## 📸 Capturas de pantalla

### Pantalla principal
*(Aquí puedes añadir una imagen mostrando la interfaz inicial de la app)*

### Subida de presupuestos PDF
*(Captura del formulario para ingresar Cliente, Edificio y Número de Presupuesto)*

### Consulta de CSV con facturas y pagos
*(Ejemplo de una pregunta realizada al agente y la respuesta obtenida)*

### Resultados visuales
*(Gráficos generados con Matplotlib sobre pagos y facturación)*

---

## ⚙️ Instalación y despliegue

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tuusuario/tu-repo.git
   cd tu-repo
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
2. Ejecutar la aplicación:
   ```bash
   streamlit run app.py
   

 
---

## 📌 Notas

- Asegúrate de incluir **langchain-experimental** en tu `requirements.txt` para habilitar el **SemanticChunker**.  
- El proyecto está diseñado para funcionar en **Python 3.12**.  
- Se recomienda usar un entorno virtual para evitar conflictos de dependencias.

---

## 🧠 Próximos pasos

- Añadir más fuentes de datos (Excel, APIs externas).  
- Mejorar la visualización de resultados con dashboards interactivos.  
- Extender el agente para responder preguntas más complejas combinando múltiples fuentes.

