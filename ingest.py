# This file loads the PDF ,splits it, embedding and store in vector  database

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_community.vectorstores import FAISS

# step 1: Load the PDF (Fixing variable name and class spelling)
loader = PyPDFLoader(r"data/FinSight_AI_Company_Policy_Handbook_v1.pdf")
documents = loader.load()

# step 2: split it into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)

print(len(chunks))


# step 3: Create the Embdings models
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# step4: Create the vector database and store the embeddings
vectorstore = FAISS.from_documents(
chunks, embeddings
)

# step 5: Save the vector database 
vectorstore.save_local("vectorstore")
print("Vector Database Created Successfully.")


