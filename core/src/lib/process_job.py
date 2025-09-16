import json
import requests
import functools
from io import BytesIO
from PyPDF2 import  PdfReader
from langgraph.graph import START , StateGraph
from .rag_pipeline import generate, retrieve , State
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_job(body: bytes , vector_store : InMemoryVectorStore):
    job = json.loads(body.decode("utf-8"))
    job_id = job["jobId"]
    job_query = job["query"]
    
    print(f"\n[*] Job Received: {job_id}")

    for idx, f in enumerate(job["files"], start=1):
        url = f["url"]
        fmt = f.get("format", "").lower()

        print(f" [*] downloading {fmt} from {url}")
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()

        if fmt == "pdf":
            reader = PdfReader(BytesIO(resp.content))

            text = "\n".join(page.extract_text() or "" for page in reader.pages)

        else:
            text = f"[Unsupported format: {fmt}]"
            print(f" [*] Unsupported format: {fmt}")

        splitter = RecursiveCharacterTextSplitter(chunk_size=800,
                                                  chunk_overlap=200)
        chunks = splitter.split_text(text)

        vector_store.add_texts(texts=chunks)

        graph_builder = StateGraph(State)
        graph_builder.add_node("retrieve", functools.partial(retrieve, vector_store=vector_store))
        graph_builder.add_node("generate", generate)
        graph_builder.add_edge(START, "retrieve")
        graph_builder.add_edge("retrieve", "generate")
        graph = graph_builder.compile()
        result = graph.invoke({"question":job_query})
        
        return {
            "jobId": job_id,
            "result": result["answer"]
        } 
        