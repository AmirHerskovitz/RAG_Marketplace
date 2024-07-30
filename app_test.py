import streamlit as st
from llama_index.legacy import VectorStoreIndex
from llama_index.legacy.llms import Ollama
from langchain.memory import ChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import ServiceContext
from llama_index.core import SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.core.llms import MockLLM
from llama_index.legacy.readers import Document  # Adjust this import based on the actual library structure

# Set up the Streamlit app
st.title("Azure Marketplace Chat")
st.caption("Chat with Azure Marketplace data using LLaMA and RAG")

# Load the data from the specified text file
data_path = "C:\\Projects\\Marketplace_Info_Center\\Data\\test.txt"

# Configure Settings
Settings.llm = Ollama(model="llama3", request_timeout=360.0)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.num_output = 512
Settings.context_window = 4096  # Example context window size
Settings.chunk_size = 1024

# Use SimpleDirectoryReader to process the content
documents = SimpleDirectoryReader(input_files=[data_path]).load_data()

# Create the vector store index
index = VectorStoreIndex.from_documents(documents=documents, embed_model=Settings.embed_model)
query_engine = index.as_query_engine(llm=MockLLM())

# Create a text input box for user queries
query = st.text_input("Ask a question about Azure Marketplace")
if query:
    response = query_engine.query(query)
    st.write(response)

# Example completion query
response = Settings.llm.complete("Who is Laurie Voss? write in 10 words")
print(response)