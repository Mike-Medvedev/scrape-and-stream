import os
import faiss
import tkinter as tk
from tkinter import scrolledtext
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

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
            print(f"Here is rag, {vector_store.search(
                'mantine stepper', search_type='mmr')}")
            print("FAISS index loaded successfully from disk.")
        except Exception as e:
            print(f"Error loading FAISS index: {e}")
    else:
        raise FileNotFoundError(
            "No FAISS index found. Please make sure you've saved the FAISS index first."
        )


# Function to query the LLM with retrieved documents
def query_llm_with_retriever(query):
    try:
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
    except Exception as e:
        return f"Error querying LLM: {e}"


# Tkinter GUI setup
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat with FAISS and OpenAI")

        # Chat display area (scrolled text)
        self.chat_display = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, height=40, width=40, state='disabled')
        self.chat_display.pack(pady=10)

        # User input area
        self.user_input = tk.Entry(root, width=40)
        self.user_input.pack(side=tk.LEFT, padx=10, pady=10)

        # Send button
        self.send_button = tk.Button(
            root, text="Send", command=self.process_query)
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def append_chat(self, text):
        """Appends text to the chat display."""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, text + "\n")
        self.chat_display.yview(tk.END)
        self.chat_display.config(state='disabled')

    def process_query(self):
        """Handles sending the user query and displaying the response."""
        query = self.user_input.get()
        if not query:
            return

        # Display the user's query
        self.append_chat(f"You: {query}")

        # Query the LLM with the user's question
        response = query_llm_with_retriever(query)

        # Display the response from the LLM
        self.append_chat(f"Bot: {response}")

        # Clear the user input
        self.user_input.delete(0, tk.END)


# Main function to start the chat app
if __name__ == "__main__":
    # Load the vector store (FAISS index)
    try:
        load_vector_store()
    except FileNotFoundError as e:
        print(e)
        exit(1)

    # Create the main window
    root = tk.Tk()

    # Create and run the chat application
    app = ChatApp(root)
    root.mainloop()
