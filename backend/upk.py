import pickle

with open('faiss_index_store/index.pkl', 'rb') as file:
    data = pickle.load(file)

print(data)
