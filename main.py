from rag import ask

while True:
    question = input("Enter your question (or 'quit' to exit): ")
    if question.lower() == "quit":
        break
    response = ask(question)
    print(response["answer"])
    print("\nSources: pages", response["pages"])
