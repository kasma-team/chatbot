import pinecone
from sentence_transformers import SentenceTransformer
from api.utils.grok_client import call_grok
import os

# Initialize Pinecone and SentenceTransformer
pc = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("faqs")
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_response(query):
    # Embed the query
    query_vector = model.encode(query).tolist()
    
    # Search Pinecone for similar FAQs
    results = index.query(vector=query_vector, top_k=1, include_metadata=True)
    
    if results.matches:
        match = results.matches[0]
        if match.score > 0.8:  # Similarity threshold
            return match.metadata["answer"]  # Assumes answer is in metadata
    
    # If no match, call Grok
    return call_grok(query)