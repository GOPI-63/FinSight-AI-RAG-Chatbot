
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS

# Step 1: Load environment variables
load_dotenv()

# Step 2: Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Step 3: Load FAISS vector database
vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

# Step 4: Create retriever
retriever = vectorstore.as_retriever()

# Step 5: Initialize LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

# Step 6: Chatbot loop
while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    # Retrieve relevant documents
    documents = retriever.invoke(question)

    # Convert documents into context
    context = "\n\n".join(
        [doc.page_content for doc in documents]
    )

    # Final prompt
    final_prompt = f"""
    You are a helpful company policy assistant.

    Answer the user's question using only the provided context.

    If the answer is not in the context, say:
    "I don't know based on the provided document."

    Context:
    {context}

    Question:
    {question}
    """

    # Generate answer
    response = llm.invoke(final_prompt)

    print("AI:", response.content)
