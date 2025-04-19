import openai
import time
import os
from dotenv import load_dotenv
from typing import List, Dict
import json
from chunker import Chunk

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')  # this is also the default, it can be omitted
)

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """Get embedding for a text chunk"""
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

def embed_chunks(chunks: List[Chunk], output_file: str = "embeddings.json") -> List[Dict]:
    """Embed all chunks and save results"""
    embeddings = []
    total_chunks = len(chunks)
    
    print(f"Starting to embed {total_chunks} chunks...")
    
    for i, chunk in enumerate(chunks):
        try:
            # Get embedding
            vector = get_embedding(chunk.text)
            
            # Create embedding record
            embedding_record = {
                "text": chunk.text,
                "embedding": vector,
                "metadata": chunk.metadata,
                "start_char": chunk.start_char,
                "end_char": chunk.end_char
            }
            
            embeddings.append(embedding_record)
            
            # Print progress
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{total_chunks} chunks")
            
            # Sleep to avoid rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error on chunk {i}: {e}")
            continue
    
    # Save embeddings to file
    with open(output_file, 'w') as f:
        json.dump(embeddings, f)
    
    print(f"\nEmbeddings saved to {output_file}")
    return embeddings

if __name__ == "__main__":
    # Import chunks from process_docs.py
    from process_docs import process_document
    
    # Process document and get chunks
    file_path = "data/openai_api_docs.txt"
    chunks = process_document(file_path)
    
    # Embed chunks
    embeddings = embed_chunks(chunks) 