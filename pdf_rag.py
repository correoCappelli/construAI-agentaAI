import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def answer_question(rag_chain, question: str):
    return rag_chain.invoke(question)

def build_rag_pipeline():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
    vector_store = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

    loader = DirectoryLoader("contenido", glob="*.pdf", loader_cls=PyPDFLoader)
    pdfs = loader.load()

    for doc in pdfs:
        filename = os.path.basename(doc.metadata.get("source", ""))
        doc.metadata["filename"] = filename
        parts = filename.replace(".pdf", "").split("_")
        if len(parts) >= 3:
            doc.metadata["presupuesto"] = parts[0]
            doc.metadata["cliente"] = parts[1]
            doc.metadata["obra"] = parts[2]
        # Inyectar metadatos e instrucción explícita
        doc.page_content = (
            f"Archivo: {filename}\n"
            f"Cliente: {doc.metadata.get('cliente','')}, "
            f"Presupuesto: {doc.metadata.get('presupuesto','')}, "
            f"Obra: {doc.metadata.get('obra','')}\n\n"
            f"IMPORTANTE: Extrae SOLO los importes monetarios de este cliente/presupuesto "
            f"(ej. 'valor', 'importe', 'anticipo', 'saldo').\n\n"
            f"{doc.page_content}"
        )

    # Splitter semántico en lugar de RecursiveCharacterTextSplitter
    splitter = SemanticChunker(
        embeddings,
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=95
    )
    chunks = splitter.split_documents(pdfs)

    if chunks:
        vector_store.add_documents(chunks)
        vector_store.persist()

    # Retriever con más contexto
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    prompt = ChatPromptTemplate.from_messages([
        ("system", """Eres un organizador de presupuestos de construcción.
        Reglas:
        - Responde SIEMPRE en dos partes:
            1. Una tabla con columnas [Cliente, Presupuesto N°, Fecha, Importe Total, Anticipo, Saldo].
            2. Una explicación detallada en lenguaje humano.
        - Debes identificar y mostrar explícitamente todos los importes monetarios encontrados en el texto (ej. "El valor total es $320.000").
        - Si hay desglose de pagos (anticipo, saldo), inclúyelos en la tabla y en la explicación.
        - Si la pregunta menciona un cliente o presupuesto específico, responde únicamente con datos de ese documento.
        - Ignora importes de otros clientes/presupuestos aunque aparezcan en el contexto.
        - Si no encuentras un importe, indica claramente "no disponible" y explica por qué.
        - Usa frases completas y claras, no respuestas telegráficas.
        """),
        ("human", "Pregunta: {query}\n\nContexto:\n{contexto}")
    ])

    modelo = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

    rag_chain = (
        {"query": RunnablePassthrough(), "contexto": retriever}
        | prompt
        | modelo
        | StrOutputParser()
    )
    return rag_chain
