import re
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Chunk:
    """Represents a chunk of text with metadata"""
    text: str
    metadata: Dict[str, Any]
    start_char: int
    end_char: int

class TextChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_by_characters(self, text: str, doc_id: str = None) -> List[Chunk]:
        """Split text into chunks of fixed size with overlap"""
        chunks = []
        start = 0
        
        while start < len(text):
            # Calculate end position with overlap
            end = start + self.chunk_size
            
            # If this is not the first chunk, include overlap
            if start > 0:
                start = start - self.chunk_overlap
            
            # Extract chunk
            chunk_text = text[start:end]
            
            # Create chunk with metadata
            chunk = Chunk(
                text=chunk_text,
                metadata={
                    "doc_id": doc_id,
                    "strategy": "character",
                    "chunk_size": self.chunk_size,
                },
                start_char=start,
                end_char=end
            )
            chunks.append(chunk)
            
            # Move to next chunk
            start = end
            
            # Break if we've reached the end
            if start >= len(text):
                break
        
        return chunks

    def chunk_by_sentences(self, text: str, doc_id: str = None) -> List[Chunk]:
        """Split text into chunks by sentences"""
        # Simple sentence detection (can be improved with nltk)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = []
        current_length = 0
        start_char = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            # If adding this sentence would exceed chunk size
            if current_length + sentence_length > self.chunk_size and current_chunk:
                # Create chunk from accumulated sentences
                chunk_text = ' '.join(current_chunk)
                end_char = start_char + len(chunk_text)
                
                chunk = Chunk(
                    text=chunk_text,
                    metadata={
                        "doc_id": doc_id,
                        "strategy": "sentence",
                        "chunk_size": self.chunk_size,
                    },
                    start_char=start_char,
                    end_char=end_char
                )
                chunks.append(chunk)
                
                # Start new chunk with overlap
                overlap_text = ' '.join(current_chunk[-2:])  # Keep last 2 sentences
                current_chunk = [overlap_text]
                current_length = len(overlap_text)
                start_char = end_char - len(overlap_text)
            
            current_chunk.append(sentence)
            current_length += sentence_length + 1  # +1 for space
        
        # Don't forget the last chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunk = Chunk(
                text=chunk_text,
                metadata={
                    "doc_id": doc_id,
                    "strategy": "sentence",
                    "chunk_size": self.chunk_size,
                },
                start_char=start_char,
                end_char=start_char + len(chunk_text)
            )
            chunks.append(chunk)
        
        return chunks

    def chunk_by_paragraphs(self, text: str, doc_id: str = None) -> List[Chunk]:
        """Split text into chunks by paragraphs"""
        # Split text into paragraphs (double newline)
        paragraphs = re.split(r'\n\s*\n', text)
        chunks = []
        current_chunk = []
        current_length = 0
        start_char = 0
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
                
            para_length = len(paragraph)
            
            # If adding this paragraph would exceed chunk size
            if current_length + para_length > self.chunk_size and current_chunk:
                # Create chunk from accumulated paragraphs
                chunk_text = '\n\n'.join(current_chunk)
                end_char = start_char + len(chunk_text)
                
                chunk = Chunk(
                    text=chunk_text,
                    metadata={
                        "doc_id": doc_id,
                        "strategy": "paragraph",
                        "chunk_size": self.chunk_size,
                    },
                    start_char=start_char,
                    end_char=end_char
                )
                chunks.append(chunk)
                
                # Start new chunk
                current_chunk = []
                current_length = 0
                start_char = end_char + 2  # +2 for double newline
            
            current_chunk.append(paragraph)
            current_length += para_length + 2  # +2 for paragraph separator
        
        # Don't forget the last chunk
        if current_chunk:
            chunk_text = '\n\n'.join(current_chunk)
            chunk = Chunk(
                text=chunk_text,
                metadata={
                    "doc_id": doc_id,
                    "strategy": "paragraph",
                    "chunk_size": self.chunk_size,
                },
                start_char=start_char,
                end_char=start_char + len(chunk_text)
            )
            chunks.append(chunk)
        
        return chunks

# Example usage
if __name__ == "__main__":
    # Test text
    test_text = """This is the first paragraph. It has multiple sentences. Each sentence adds more context.

    This is the second paragraph. It continues the example. We'll use this to test our chunking.

    Finally, this is the third paragraph. It will help demonstrate paragraph-based chunking."""
    
    chunker = TextChunker(chunk_size=100, chunk_overlap=20)
    
    print("Character-based chunks:")
    char_chunks = chunker.chunk_by_characters(test_text, "test_doc")
    for i, chunk in enumerate(char_chunks):
        print(f"\nChunk {i + 1}:")
        print(f"Text: {chunk.text}")
        print(f"Start: {chunk.start_char}, End: {chunk.end_char}")
    
    print("\nSentence-based chunks:")
    sent_chunks = chunker.chunk_by_sentences(test_text, "test_doc")
    for i, chunk in enumerate(sent_chunks):
        print(f"\nChunk {i + 1}:")
        print(f"Text: {chunk.text}")
        print(f"Start: {chunk.start_char}, End: {chunk.end_char}")
    
    print("\nParagraph-based chunks:")
    para_chunks = chunker.chunk_by_paragraphs(test_text, "test_doc")
    for i, chunk in enumerate(para_chunks):
        print(f"\nChunk {i + 1}:")
        print(f"Text: {chunk.text}")
        print(f"Start: {chunk.start_char}, End: {chunk.end_char}") 