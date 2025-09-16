from typing import TypedDict, List
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from utils.prompt import prompt

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def retrieve(state: State, vector_store: InMemoryVectorStore):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}
