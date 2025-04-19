import requests
import os
from bs4 import BeautifulSoup

def download_api_reference():
    """Download OpenAI API reference"""
    url = "https://platform.openai.com/docs/api-reference"
    
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    
    try:
        print("Downloading API reference...")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Break into lines and remove leading/trailing space
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Save to file
        with open("data/openai_api-reference.txt", 'w', encoding='utf-8') as f:
            f.write(text)
        print("Saved to data/openai_api-reference.txt")
        
    except Exception as e:
        print(f"Error downloading API reference: {e}")

if __name__ == "__main__":
    download_api_reference() 