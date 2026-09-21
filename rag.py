from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
import os

provider = os.getenv("PROVIDER", "ollama")

if provider == "groq":
    from langchain_groq import ChatGroq
    model = ChatGroq(model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"))
else:
    model = OllamaLLM(model="llama3.2")

template = """
You are an expert in commercial driver licensing.
Answer only from the context below. If the answer is not there, say you don't know.

Context: {context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model   #the prompt's output feeds into the model.


def ask(question):
    docs = retriever.invoke(question)
    result = chain.invoke({"context": docs, "question": question})
    answer = getattr(result, "content", result)
    pages = sorted(set(d.metadata["page"] + 1 for d in docs))
    return {"answer": answer, "pages": pages}
