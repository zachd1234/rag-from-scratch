import faiss
import numpy as np
import json
import openai
import os
from dotenv import load_dotenv
from typing import List, Dict, Tuple

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """Get embedding for a query text"""
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

def load_faiss_index(index_path: str = "faiss_index.bin") -> faiss.IndexFlatL2:
    """Load the FAISS index from file"""
    return faiss.read_index(index_path)

def load_chunk_metadata(metadata_path: str = "chunk_metadata.json") -> List[Dict]:
    """Load chunk metadata from file"""
    with open(metadata_path, 'r') as f:
        return json.load(f)

def search_similar_chunks(query: str, k: int = 5) -> Tuple[List[Dict], List[float]]:
    """
    Search for similar chunks using FAISS
    Returns:
        - List of top-k similar chunks with their metadata
        - List of corresponding distances
    """
    # Get query embedding
    query_embedding = get_embedding(query)
    query_vector = np.array([query_embedding]).astype('float32')
    
    # Load FAISS index
    index = load_faiss_index()
    
    # Search for similar vectors
    distances, indices = index.search(query_vector, k)
    
    # Load chunk metadata
    metadata = load_chunk_metadata()
    
    # Get top-k chunks using dictionary access
    top_chunks = [metadata[str(int(idx))] for idx in indices[0]]
    
    return top_chunks, distances[0].tolist()

def format_context(chunks: List[Dict]) -> str:
    """Format retrieved chunks into a context string"""
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"Chunk {i+1}:\n{chunk['text']}\n\n"
    return context.strip()

def query_and_retrieve(query: str, k: int = 5) -> Tuple[str, List[float]]:
    """
    Main function to process query and retrieve relevant chunks
    Returns:
        - Formatted context string
        - List of distances for retrieved chunks
    """
    # Search for similar chunks
    chunks, distances = search_similar_chunks(query, k)
    
    # Format chunks into context
    context = format_context(chunks)
    
    return context, distances

def generate_answer(query: str, context: str) -> str:
    """
    Generate an answer using the retrieved context and OpenAI's chat completion
    """
    system_prompt = """You are a highly accurate assistant. Use ONLY the context below to answer the user's question. 
    If the answer cannot be found in the context, respond with: "I don't know based on the provided information."
    Do not make up or guess information. Be precise and factual."""
    
    user_prompt = f"""Context information is below.
    ---------------------
    {context}
    ---------------------
    Given ONLY the context information above and no prior knowledge, answer the question: {query}"""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3  # Lower temperature for more focused, deterministic responses
    )
    
    return response.choices[0].message.content

def query_and_answer(query: str, k: int = 5) -> Tuple[str, str, List[float]]:
    """
    Complete pipeline: query, retrieve context, and generate answer
    Returns:
        - Generated answer
        - Retrieved context
        - List of distances for retrieved chunks
    """
    # Get context and distances
    context, distances = query_and_retrieve(query, k)
    
    # Generate answer
    answer = generate_answer(query, context)
    
    return answer, context, distances

if __name__ == "__main__":
    # Example usage
    query = "Who is the CEO of Anthropic?"
    answer, context, distances = query_and_answer(query)
    
    print("\nQuestion:")
    print(query)
    print("\nRetrieved Context:")
    print(context)
    print("\nAnswer:")
    print(answer)
    print("\nDistances:")
    print(distances) 