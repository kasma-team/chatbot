# import os
# from pinecone import Pinecone
# from sentence_transformers import SentenceTransformer
# from dotenv import load_dotenv
# import json

# load_dotenv()

# def load_faqs():
#     # Initialize Pinecone with new API
#     pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    
#     # Initialize the index
#     index = pc.Index("faqs")
    
#     # Initialize the sentence transformer model
#     model = SentenceTransformer("all-MiniLM-L6-v2")
    
#     # Sample FAQs - replace these with your actual FAQs
#     faqs = 'data/faqs.json'
#     with open(faqs, 'r', encoding='utf-8') as f:
#         faqs = json.load(f)
    
#     # Prepare vectors for Pinecone
#     vectors = []
#     for faq in faqs:
#         # Encode the question
#         vector = model.encode(faq["question"]).tolist()
        
#         # Create metadata
#         metadata = {
#             "question": faq["question"],
#             "answer": faq["answer"]
#         }
        
#         # Add to vectors list
#         vectors.append((faq["id"], vector, metadata))
    
#     # Upsert vectors to Pinecone
#     index.upsert(vectors=vectors)
#     print("FAQs loaded successfully!")

# if __name__ == "__main__":
#     load_faqs()