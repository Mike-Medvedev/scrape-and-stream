import faiss

# Load the FAISS index from the correct file
faiss_index_file = "faiss_index_store/index.faiss"
index = faiss.read_index(faiss_index_file)

# Get the number of vectors (N) and dimensionality (D)
n_vectors = index.ntotal  # Total number of vectors in the index
d = index.d  # Dimensionality of each vector

print(f"Number of vectors in the index: {n_vectors}")
print(f"Dimensionality of the vectors: {d}")
