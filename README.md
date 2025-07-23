# 🌐 URL-based RAG Chatbot with Persona

This project is a modern, session-based web chatbot that allows users to:
- Input a URL and a custom assistant persona
- Automatically fetch and chunk web content using LangChain
- Embed content with HuggingFace Sentence Transformers
- Perform similarity search and respond using Groq LLM API
- Chat in a modern interface with saved history and Excel export

---

## 🚀 Features

✅ URL-based RAG with HuggingFace Embeddings  
✅ Persona-driven Groq LLM response logic  
✅ Two-page UI: URL + Persona form → Chat UI  
✅ Session ID for isolated chat history  
✅ `localStorage` chat saving across reloads  
✅ Smooth scrolling, clean UI, Excel chat export  

---

## 📁 Files Overview

- `index.html` — Page 1: URL and persona input  
- `chat.html` — Page 2: Chat interface  
- `style.css` — Modern styling shared by both pages  
- `backend.py` — Flask backend handling all endpoints  
- `ChatbotWithUrl.py` — Web content processing + embedding logic

---

## 🐍 Requirements

**Python 3.10.x is required.**

### 🔧 Setup Instructions

1. **Create a virtual environment:**
```bash
python3.10 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install flask flask-cors langchain-community langchain_huggingface \
sentence-transformers chromadb beautifulsoup4 python-dotenv pandas openpyxl
```

3. **Set your Groq API key** directly in `backend.py` or `ChatbotWithUrl.py` where the `Groq` client is initialized.

---

## ▶️ Run the Application

```bash
python backend.py
```

Flask will start on: `http://localhost:5000`

Then open `index.html` in your browser to begin.

(Optional) Serve HTML with:
```bash
python3 -m http.server 5500
```

Visit: `http://localhost:5500/index.html`

---

## 🧪 API Endpoints

- `POST /upload_url` — Load & embed URL content  
- `POST /query` — Chat query + Groq response  
- `GET /new_session` — Generate new session ID  
- `POST /export_chat` — Export chat to Excel  
- `GET /health` — Check service status  

---


## ✨ Possible Improvements

- RAG file upload hybrid (URL + PDF)
- LLM streaming for faster response feel
- Better error handling for CORS/Timeouts
- User login and saved conversation history

---

## 🤝 Credits

- 🧠 [LangChain](https://github.com/langchain-ai/langchain)
- 🤗 [HuggingFace](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- 💬 [Groq API](https://console.groq.com/)
- 🧽 [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
