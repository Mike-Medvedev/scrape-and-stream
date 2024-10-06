import os
import json
import faiss
import asyncio
from urllib.parse import urljoin, urlparse
from pyppeteer import launch
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore

client = OpenAI()

# Set up embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# Folder path for saving FAISS index and metadata
folder_path = "faiss_index_store"
index_name = "index"

# Load FAISS index if it exists, otherwise initialize a new one
if os.path.exists(folder_path):
    vector_store = FAISS.load_local(
        folder_path=folder_path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True  # Allow this only if you trust the source
    )
    print("Loaded existing FAISS index from disk.")
else:
    # Initialize new FAISS vector store with InMemoryDocstore
    vector_store = FAISS(
        embedding_function=embeddings,
        index=faiss.IndexFlatL2(1536),
        docstore=InMemoryDocstore({}),  # Use an empty in-memory docstore
        index_to_docstore_id={}         # Initialize an empty mapping
    )
    print("Created new FAISS index.")

# Allowed paths
allowed_paths = [
    "styles", "theming", "guides", "hooks", "form", "core", "dates", "charts", "x"
]

# Async function to scrape a website


async def browse_website(url):
    browser = await launch(headless=True)
    page = await browser.newPage()

    visited_urls = set()  # Track visited URLs
    to_visit = [url]  # Queue of URLs to visit

    while to_visit:
        current_url = to_visit.pop(0)

        if current_url in visited_urls:
            continue

        visited_urls.add(current_url)

        try:
            await page.goto(current_url, {'timeout': 60000, 'waitUntil': 'networkidle0'})
            print(f"Scraping: {current_url}")
            text_content = await page.evaluate('document.body.innerText')

            # Add text content and metadata to vector store
            vector_store.add_texts([text_content], metadatas=[
                                   {"url": current_url}])

            # Extract internal links
            links = await page.evaluate('''() => {
                const anchorTags = document.querySelectorAll('a');
                return Array.from(anchorTags).map(a => a.href);
            }''')

            parsed_base = urlparse(url)
            base_url = f"{parsed_base.scheme}://{parsed_base.netloc}"

            for link in links:
                parsed_link = urlparse(link)
                normalized_url = urljoin(base_url, parsed_link.path)

                # Filter URLs by allowed paths
                if (
                    any(normalized_url.startswith(urljoin(base_url, f"/{path}/")) for path in allowed_paths) and
                    normalized_url not in visited_urls
                ):
                    to_visit.append(normalized_url)

        except Exception as e:
            print(f"Error scraping {current_url}: {e}")

    await browser.close()


def save_vector_store():
    vector_store.save_local(folder_path, index_name=index_name)
    print(f"Vector store and metadata saved to {folder_path}.")

# Function to query the LLM

# Function to answer a query based on the stored vectors


# Inspect the vector store and log results to a file

# Main function
if __name__ == "__main__":
    website_url = input("Enter the website URL to scrape: ")

    try:
        asyncio.run(browse_website(website_url))
        save_vector_store()  # Save FAISS index and metadata after scraping
    except Exception as e:
        print(f"Error during execution: {e}")
