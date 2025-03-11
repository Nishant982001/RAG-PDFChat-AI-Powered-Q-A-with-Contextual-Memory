# RAG-PDFChat: AI-Powered Q&A with Contextual Memory
1. Overview
RAG-PDFChat is an advanced AI-powered chatbot that enables context-aware question answering over PDFs using Retrieval-Augmented Generation (RAG). It combines LangChain, ChromaDB, Groq API (Gemma-2B-IT), and Hugging Face embeddings to provide precise, multi-turn responses while maintaining chat history for contextual memory.

2. Key Features:
✅ Ask AI questions about PDFs with LLM-powered retrieval
✅ Uses ChromaDB for vector storage & efficient document retrieval
✅ Chat history retention for multi-turn conversations
✅ Customizable API key input for flexibility
✅ Optimized with advanced prompt engineering for high-quality responses

📂 Project Structure
📁 RAG-PDFChat
│── 📜 README.md
│── 📜 requirements.txt
│── 📜 app.py  # Main application logic
│── 📜 pdf_processing.py  # Extracts and splits PDF text
│── 📜 retriever.py  # RAG-based document retrieval
│── 📜 chat_memory.py  # Manages multi-turn chat history
│── 📁 data/  # Stores uploaded PDFs
│── 📁 models/  # (Optional) LLM fine-tuning files

3. Installation & Setup
i] Install Dependencies
Ensure you have Python 3.8+, then run:
pip install -r requirements.txt

ii] Set Up Environment Variables
Create a .env file and add your API keys:
OPENAI_API_KEY="your-api-key-here"
HF_TOKEN="your-huggingface-token-here"

iii] Run the Application
python app.py
Or, if using Streamlit UI:
streamlit run app.py

iv] Upload a PDF & Start Chatting!
Upload a PDF document
Enter your Groq API Key
Ask questions & get AI-generated responses

4. How It Works
1️ PDF Ingestion → Extracts text using PyPDFLoader
2️ Text Chunking & Embedding → Splits text into 5,000-character chunks & encodes them with Hugging Face embeddings
3️ Vector Storage & Retrieval → Stores embeddings in ChromaDB and retrieves relevant chunks
4️ LLM-Powered Q&A → Uses Groq API (Gemma-2B-IT) to generate responses
5️ Chat Memory Management → Retains previous messages for contextual multi-turn conversations

5. Technologies Used
Category	Technologies
Programming :	Python, Streamlit
LLMs & Embeddings : 	Groq API (Gemma-2B-IT), Hugging Face Embeddings
Retrieval & Storage : LangChain, ChromaDB, Recursive Text Splitters
Document Processing : PyPDFLoader
Prompt Engineering : Context-aware question formulation, response optimization

6. Future Enhancements
🔹 Multi-PDF Querying → Ask questions across multiple documents
🔹 Hybrid Search (BM25 + Vector Search) → Improve retrieval accuracy
🔹 Cloud Deployment (AWS/GCP) → Make the app scalable
🔹 Fine-Tuned Models for Domain-Specific Use Cases

7. License
This project is open-source under the MIT License.

Want to improve this project? Fork it, experiment, and contribute! 🚀🔥
