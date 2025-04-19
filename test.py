from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.settings import Settings
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up LLM with API key
llm = OpenAI(
    model="gpt-3.5-turbo",
    api_key=os.getenv('OPENAI_API_KEY')  # Get API key from environment
)

# Configure settings
Settings.llm = llm

# Load documents from a directory
documents = SimpleDirectoryReader("data").load_data()

# Build index
index = VectorStoreIndex.from_documents(documents)

# Query engine
query_engine = index.as_query_engine()

# Ask a question
response = query_engine.query("What is Paul Graham's advice for startup founders?")
print(response)
