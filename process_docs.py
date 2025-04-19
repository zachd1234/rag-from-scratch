from chunker import TextChunker
import os
from typing import List, Dict

def load_document(file_path: str) -> str:
    """Load a document from file"""
    print(f"\nFile info:")
    print(f"File size: {os.path.getsize(file_path)} bytes")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"Number of lines: {len(content.splitlines())}")
        print(f"Total characters: {len(content)}")
        return content

def process_document(file_path: str, chunk_size: int = 500, chunk_overlap: int = 100):
    """Process a single document"""
    chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    print(f"\nProcessing {file_path}...")
    
    # Load and chunk document
    text = load_document(file_path)
    chunks = chunker.chunk_by_characters(text, "api_reference")
    
    print(f"Created {len(chunks)} chunks")
    return chunks

def analyze_chunks(chunks: List[Dict]):
    """Print analysis of chunks"""
    print("\nChunk Analysis:")
    print(f"Total chunks: {len(chunks)}")
    
    # Analyze chunk sizes
    sizes = [len(chunk.text) for chunk in chunks]
    avg_size = sum(sizes) / len(sizes)
    max_size = max(sizes)
    min_size = min(sizes)
    
    print(f"Average chunk size: {avg_size:.2f} characters")
    print(f"Max chunk size: {max_size}")
    print(f"Min chunk size: {min_size}")

if __name__ == "__main__":
    # Process single document
    file_path = "data/openai_api_docs.txt"  # Using the new file
    chunks = process_document(file_path)
    
    # Analyze results
    analyze_chunks(chunks)
    
    # Print first few chunks as example
    print("\nExample chunks:")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {i + 1}:")
        print(f"Text length: {len(chunk.text)} characters")
        print(f"Metadata: {chunk.metadata}")
        print(f"First 100 characters: {chunk.text[:100]}...") 