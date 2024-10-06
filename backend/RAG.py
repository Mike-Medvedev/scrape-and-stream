import os
from typing import List
import faiss
from fastapi import HTTPException
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

# Initialize the OpenAI LLM client
client = OpenAI()


# Define the path for the FAISS index
folder_path = "faiss_index_store"
index_name = "index"

# Initialize the FAISS vector store
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")


def load_vector_store():
    global vector_store
    if os.path.exists(folder_path):
        try:
            # Load the FAISS index from the folder
            vector_store = FAISS.load_local(
                folder_path=folder_path,
                embeddings=embeddings,
                allow_dangerous_deserialization=True
            )
            print("FAISS index loaded successfully from disk.")
        except Exception as e:
            print(f"Error loading FAISS index: {e}")
    else:
        raise FileNotFoundError(
            "No FAISS index found. Please make sure you've saved the FAISS index first."
        )


# Function to query the LLM with retrieved documents
def query_llm_with_retriever(query):
    # Generate the embedding for the query using the same embeddings model
    query_embedding = embeddings.embed_query(query)

    # Retrieve relevant documents based on the query
    similar_texts = vector_store.similarity_search_by_vector(
        query_embedding)
    # Combine the content of the retrieved documents
    combined_content = ""
    for doc in similar_texts:
        url = doc.metadata.get('url', 'Unknown URL')
        combined_content += f"Content from {url}: {doc.page_content}\n"

    # Prepare the prompt for the LLM
    prompt = [
        {"role": "system", "content": "You are an assistant that answers questions based on the provided context."},
        {"role": "user", "content": f"""Context:\n{
            combined_content}\n\nQuestion:\n{query}"""}
    ]

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=prompt
    )
    return completion.choices[0].message.content


class Message(BaseModel):
    role: str
    content: str


async def query_llm_with_retriever_for_api(query: List[Message]):
    load_vector_store()
    try:

        if not query:
            raise ValueError("Query list is empty")
        # Generate the embedding for the query using the same embeddings model
        latest_message = query[-1].content
        query_embedding = embeddings.embed_query(latest_message)

        # Retrieve relevant documents based on the query
        similar_texts = vector_store.similarity_search_by_vector(
            query_embedding)
        # Combine the content of the retrieved documents
        combined_content = ""
        for doc in similar_texts:
            url = doc.metadata.get('url', 'Unknown URL')
            combined_content += f"Content from {url}: {doc.page_content}\n"

        # Prepare the prompt for the LLM
        prompt = [
            {"role": "system", "content": "You are an assistant that answers questions based on the provided context."},
            {"role": "user", "content": f"""Context:\n{
                combined_content}\n\nQuestion:\n{latest_message}"""}
        ]

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=prompt
        )
        res = completion.choices[0].message
        print(res)
        return query + [Message(role='assistant', content=completion.choices[0].message.content)]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")


# Main function to run the RAG system
if __name__ == "__main__":
    # Load the vector store (FAISS index)
    try:
        load_vector_store()
    except FileNotFoundError as e:
        print(e)
        exit(1)

    # Input query from the user
    user_query = input("Enter your question about the scraped content: ")

    # Query the LLM with the retrieved documents
    response = query_llm_with_retriever(user_query)
    print("Answer:", response)
