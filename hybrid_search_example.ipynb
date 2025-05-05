# Imports
import numpy as np
import pandas as pd
import faiss
import uuid

# Generate synthetic data
np.random.seed(42)
categories = ['electronics', 'books', 'clothing', 'sports']
n_items = 1000
embedding_dim = 128

data = {
    'item_id': [str(uuid.uuid4()) for _ in range(n_items)],
    'name': [f"Item {i}" for i in range(n_items)],
    'category': np.random.choice(categories, n_items),
    'price': np.round(np.random.uniform(10, 500, n_items), 2),
    'embedding': [np.random.rand(embedding_dim).astype('float32') for _ in range(n_items)]
}

df = pd.DataFrame(data)

# Normalize embeddings
embeddings = np.vstack(df['embedding'].values)
norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
normalized_embeddings = embeddings / norms

# Build full Faiss index
index = faiss.IndexFlatIP(embedding_dim)
index.add(normalized_embeddings)

# Hybrid Query Example
query_vector = np.random.rand(embedding_dim).astype('float32')
query_vector /= np.linalg.norm(query_vector)

filtered_df = df[(df['category'] == 'electronics') & (df['price'] < 100)]
filtered_embeddings = np.vstack(filtered_df['embedding'].values)
filtered_embeddings /= np.linalg.norm(filtered_embeddings, axis=1, keepdims=True)

filtered_index = faiss.IndexFlatIP(embedding_dim)
filtered_index.add(filtered_embeddings)

D, I = filtered_index.search(query_vector.reshape(1, -1), 5)
results = filtered_df.iloc[I[0]].reset_index(drop=True)
results[['item_id', 'name', 'category', 'price']]
