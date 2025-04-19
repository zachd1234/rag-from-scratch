from llama_index.core import SimpleDirectoryReader
from dotenv import load_dotenv
import os

def ensure_data_directory():
    """Ensure the data directory exists"""
    if not os.path.exists("data"):
        os.makedirs("data")
        print("Created data directory")

def load_documents(directory="data"):
    """Load documents from the specified directory using LlamaIndex's SimpleDirectoryReader"""
    return SimpleDirectoryReader(directory).load_data()

def main():
    # Ensure data directory exists
    ensure_data_directory()
    
    # Load documents
    print("Loading documents...")
    documents = load_documents()
    
    # Print document information
    print(f"\nLoaded {len(documents)} documents:")
    for i, doc in enumerate(documents):
        print(f"Document {i+1}:")
        print(f"Text length: {len(doc.text)} characters")
        print(f"Metadata: {doc.metadata}")
        print("-" * 50)

if __name__ == "__main__":
    main() 