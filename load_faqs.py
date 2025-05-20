import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

def load_faqs():
    # Initialize Pinecone with new API
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    
    # Initialize the index
    index = pc.Index("faqs")
    
    # Initialize the sentence transformer model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Sample FAQs - replace these with your actual FAQs
    faqs = [
        {
            "id": "1",
            "question": "What services do you offer?",
            "answer": "We offer a wide range of services including AI-powered chatbots, custom software development, and technical consulting."
        },
        {
            "id": "2",
            "question": "How can I get started?",
            "answer": "You can get started by contacting our sales team or filling out the contact form on our website."
        },
        {
            "id": "3",
            "question": "What is your pricing model?",
            "answer": "Our pricing is based on your specific needs and requirements. Please contact us for a custom quote."
        }
    ]
    
    # Prepare vectors for Pinecone
    vectors = []
    for faq in faqs:
        # Encode the question
        vector = model.encode(faq["question"]).tolist()
        
        # Create metadata
        metadata = {
            "question": faq["question"],
            "answer": faq["answer"]
        }
        
        # Add to vectors list
        vectors.append((faq["id"], vector, metadata))
    
    # Upsert vectors to Pinecone
    index.upsert(vectors=vectors)
    print("FAQs loaded successfully!")

if __name__ == "__main__":
    load_faqs()