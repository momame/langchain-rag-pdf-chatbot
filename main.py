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

while True:
    question = input("Enter your question (or 'quit' to exit): ")
    if question.lower() == "quit":
        break
    docs = retriever.invoke(question)
    result = chain.invoke({"context": docs, "question": question})
    print(result)
    print("\nSources: pages", [doc.metadata["page"] + 1  for doc in docs])
    
    # For debugging, you can uncomment the following lines to see the content of the retrieved documents:
    # for d in docs:
    #    print(d.metadata["page"] + 1, d.page_content[:200])