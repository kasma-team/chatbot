# NigedEase Chatbot

NigedEase is an AI-powered business management assistant designed for Ethiopian businesses. It provides a web-based chatbot interface to help users manage inventory, sales, finances, and more, replacing manual systems with a centralized, cloud-based solution.

## Features
- **Conversational Chatbot**: Answers business-related queries in English and Amharic.
- **Real-Time Inventory & Sales Reports**: Demo mode provides sample inventory and sales data.
- **Mobile-Friendly**: Accessible from smartphones and tablets.

## Project Structure
- `run.py`: Main Flask app entry point.
- `api/`: Backend logic, including chatbot service, database, and API routes.
- `data/`: Knowledge base and SQLite database.
- `templates/`: HTML templates for the chatbot and analytics dashboard.
- `static/`: CSS and JS for the frontend.

## Setup & Usage
1. **Clone the repository** and navigate to the project folder.
2. **Create a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set environment variables** (see `.env.example` or set `GROQ_API_KEY` and other keys as needed).
5. **Run the app**:
   ```bash
   python run.py
   ```
   The app will be available at `http://localhost:5001`.

## API Endpoints
- `/api/chat` (POST): Send a message to the chatbot.
- `/api/settings` (GET/POST): Get or update user language and demo mode.
- `/api/reload_kb` (POST): Reload the knowledge base.
- `/analytics`: View analytics dashboard.

## Demo Mode
Enable demo mode to see sample inventory and sales reports.

## Knowledge Base
The chatbot uses `data/knowledge_base.json` for FAQs and business info. You can extend this file to add more Q&A pairs.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

