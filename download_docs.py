import requests
import os
import time

def download_openai_docs():
    """Download OpenAI documentation pages"""
    # Create docs directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # List of documentation pages to download
    pages = [
        ("quickstart", "https://platform.openai.com/docs/quickstart"),
        ("pricing", "https://platform.openai.com/docs/pricing"),
        ("guides", "https://platform.openai.com/docs/guides"),
        ("api-reference", "https://platform.openai.com/docs/api-reference"),
        ("safety", "https://platform.openai.com/docs/safety-best-practices")
    ]
    
    for name, url in pages:
        try:
            print(f"Downloading {url}...")
            response = requests.get(url)
            
            # Save raw HTML for now
            filename = f"data/openai_{name}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"Saved to {filename}")
            
            # Be nice to the server
            time.sleep(1)
            
        except Exception as e:
            print(f"Error downloading {url}: {e}")

if __name__ == "__main__":
    download_openai_docs() 