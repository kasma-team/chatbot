import os
import json
import numpy as np
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from .database import Database

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

class ChatbotService:
    def __init__(self):
        # Initialize TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer()
        
        # Store documents and metadata
        self.documents = []
        self.metadata = []
        self.document_vectors = None
        
        # Initialize translator
        self.translator = GoogleTranslator(source='en', target='am')
        
        # Initialize database
        self.db = Database()
        
        # Load knowledge base and demo data
        self.load_knowledge_base()
        self.db.init_demo_data()

    def load_knowledge_base(self):
        try:
            with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
                kb_data = json.load(f)
            
            # Prepare documents and metadata
            documents = []
            metadata = []
            
            for item in kb_data:
                # Add English content
                documents.append(item['content'])
                metadata.append({
                    'title': item['title'],
                    'id': f"{item['id']}_en",
                    'language': 'en'
                })
                
                # Add Amharic content if available
                if 'content_am' in item:
                    documents.append(item['content_am'])
                    metadata.append({
                        'title': item['title'],
                        'id': f"{item['id']}_am",
                        'language': 'am'
                    })
            
            # Generate TF-IDF vectors
            self.document_vectors = self.vectorizer.fit_transform(documents)
            
            # Store documents and metadata
            self.documents = documents
            self.metadata = metadata
            
            print("Knowledge base loaded successfully!")
        except Exception as e:
            print(f"Error loading knowledge base: {str(e)}")

    def get_related_faqs(self, query, language='en', n=2):
        # Generate query vector
        query_vector = self.vectorizer.transform([query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, self.document_vectors).flatten()
        
        # Get top n similar documents
        top_indices = similarities.argsort()[-n:][::-1]
        
        # Filter results by language and get documents
        results = {
            'documents': [],
            'metadatas': []
        }
        
        for idx in top_indices:
            if idx < len(self.metadata) and self.metadata[idx]['language'] == language:
                results['documents'].append(self.documents[idx])
                results['metadatas'].append(self.metadata[idx])
        
        return results

    def translate_to_amharic(self, text):
        try:
            return self.translator.translate(text)
        except:
            return text

    def handle_demo_query(self, query):
        if "inventory" in query.lower():
            data = self.db.get_demo_data("inventory")
            response = "Here's the current inventory:\n"
            for branch, items in data["branches"].items():
                response += f"\n{branch}:\n"
                for item, quantity in items.items():
                    response += f"- {item}: {quantity}\n"
        elif "sales" in query.lower():
            data = self.db.get_demo_data("sales")
            response = "Here's the weekly sales report:\n"
            for branch, items in data["weekly_sales"].items():
                response += f"\n{branch}:\n"
                for item, quantity in items.items():
                    response += f"- {item}: {quantity} units sold\n"
        else:
            response = "I can show you sample inventory or sales reports. Just ask!"
        return response

    def generate_response(self, query, language='en', demo_mode=False):
        if demo_mode:
            response = self.handle_demo_query(query)
            chat_response = response
        else:
            # Get relevant context from FAISS
            context_results = self.get_related_faqs(query, language)
            context = "\n".join(context_results['documents']) if context_results['documents'] else ""
            
            # Prepare the prompt
            prompt = f"""As a helpful assistant for NigedEase, an Ethiopian business management platform, answer the following question.
            Use this context if relevant: {context}
            
            Question: {query}
            
            Provide a clear, friendly response suitable for Ethiopian business owners. If the context doesn't contain relevant information,
            provide a helpful general response about NigedEase's business management features."""

            # Generate response using Groq API via HTTP
            headers = {
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            }
            data = {
                "model": "llama3-70b-8192",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant for NigedEase, an Ethiopian business management platform."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1024
            }
            response = requests.post(GROQ_API_URL, headers=headers, json=data)
            chat_response = response.json()['choices'][0]['message']['content'] if response.ok else f"Error: {response.text}"

        # Translate to Amharic if requested
        if language == 'am':
            chat_response = self.translate_to_amharic(chat_response)
        
        # Get related questions
        related_results = self.get_related_faqs(query, language, n=2)
        related_questions = [meta['title'] for meta in related_results['metadatas']] if related_results['metadatas'] else []
        
        # Log the query
        self.db.log_query(query, chat_response, language)
        
        return {
            'response': chat_response,
            'related_questions': related_questions
        }

    def get_analytics(self):
        return self.db.get_query_stats()