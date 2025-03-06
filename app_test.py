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

# Add a sidebar with a file uploader to allow users to upload their own data files
uploaded_file = st.sidebar.file_uploader("Upload your data file", type=["txt"])
if uploaded_file is not None:
    data_path = uploaded_file

# Add a button to clear the chat history
if st.sidebar.button("Clear Chat History"):
    st.session_state["chat_history"] = []

# Add a section to display the chat history
st.subheader("Chat History")
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
for message in st.session_state["chat_history"]:
    st.write(message)

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
    st.session_state["chat_history"].append(f"User: {query}")
    st.session_state["chat_history"].append(f"Bot: {response}")
    st.write(response)

# Add a section to display the response from the query engine
st.subheader("Query Response")
if query:
    st.write(response)

# Example completion query
response = Settings.llm.complete("Who is Laurie Voss? write in 10 words")
st.subheader("Completion Query Response")
st.write(response)
