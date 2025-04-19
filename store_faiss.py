import faiss
import numpy as np
import json
from typing import List, Dict

def store_in_faiss(embeddings_file: str = "embeddings.json", 
                  index_file: str = "faiss_index.bin",
                  metadata_file: str = "chunk_metadata.json") -> None:
    """
    Store embeddings in FAISS index and save it to disk along with chunk metadata
    
    Args:
        embeddings_file: Path to the JSON file containing embeddings
        index_file: Path where to save the FAISS index
        metadata_file: Path where to save the chunk metadata mapping
    """
    # Load embeddings from file
    with open(embeddings_file, 'r') as f:
        embeddings_data = json.load(f)
    
    # Extract just the embedding vectors
    embeddings = [item['embedding'] for item in embeddings_data]
    
    # Create chunk metadata mapping
    chunk_map = {i: {
        'text': item['text'],
        'metadata': item['metadata'],
        'start_char': item['start_char'],
        'end_char': item['end_char']
    } for i, item in enumerate(embeddings_data)}
    
    # Save chunk metadata mapping
    with open(metadata_file, 'w') as f:
        json.dump(chunk_map, f)
    print(f"Chunk metadata mapping saved to {metadata_file}")
    
    # Convert to numpy array
    embedding_matrix = np.array(embeddings).astype('float32')
    
    # Get dimension from first embedding
    dimension = len(embeddings[0])
    
    # Create FAISS index
    index = faiss.IndexFlatL2(dimension)
    
    # Add vectors to index
    index.add(embedding_matrix)
    
    # Save index to disk
    faiss.write_index(index, index_file)
    print(f"FAISS index saved to {index_file}")

if __name__ == "__main__":
    store_in_faiss() 