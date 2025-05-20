from flask import Blueprint, request, jsonify
from api.services.chatbot_service import get_response

api_bp = Blueprint("api", __name__)

@api_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"error": "Query is required"}), 400
    response = get_response(query)
    return jsonify({"response": response})