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

├── app.py                # Aplicación principal en Streamlit
├── pdf_rag.py            # Pipeline RAG para PDFs
├── csv_rag.py            # Procesamiento y consultas sobre CSV
├── contenido/const_data.csv    # archivo CSV con datos de facturacion 
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Este archivo



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
   

 Notas

    -Asegúrate de incluir langchain-experimental en tu requirements.txt para habilitar el SemanticChunker.

    -El proyecto está diseñado para funcionar en Python 3.12.

    -Se recomienda usar un entorno virtual para evitar conflictos de dependencias.

Próximos pasos

    -Añadir más fuentes de datos (Excel, APIs externas).

    -Mejorar la visualización de resultados con dashboards interactivos.

    -Extender el agente para responder preguntas más complejas combinando múltiples fuentes.

