# 🌐 Website URL-Based RAG Chatbot with Persona (Full Site Crawling Enabled)

This project is a powerful RAG (Retrieval-Augmented Generation) chatbot system that crawls all internal pages of a website, extracts the text, embeds it into a vector store, and allows users to chat with the content using an intelligent assistant with a custom persona. Built using LangChain, HuggingFace Embeddings, Groq API, and Flask.

---

## 🚀 Features

- 🌍 **Crawls full websites** (not just a single URL) using `requests` + `BeautifulSoup`
- 📄 Extracts and parses HTML content using LangChain’s `WebBaseLoader`
- ✂️ Splits long documents into overlapping chunks
- 🧠 Embeds chunks using HuggingFace models into a Chroma vector store
- 🤖 Uses Groq LLM to generate accurate, contextual answers
- 🧑‍💼 Accepts a custom assistant persona
- 🧾 LocalStorage-based chat memory per session
- 💾 Chat history can be exported to `.xlsx`
- 🖥️ Modern 2-page UI (URL & Persona → Chat)

---

## 🧱 File Overview

| File                 | Description                                 |
|----------------------|---------------------------------------------|
| `backend.py`         | Flask backend with crawling and QA endpoints |
| `index.html`         | Page to input URL and persona               |
| `chat.html`          | Chat interface                              |
| `style.css`          | Modern CSS styling                          |

---

## 🐍 Requirements

- **Python 3.10.x** recommended

### 📦 Install Dependencies

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install flask flask-cors langchain-community langchain_huggingface \
sentence-transformers chromadb beautifulsoup4 python-dotenv pandas openpyxl requests
```

---

## ▶️ How to Use

1. **Run the Backend:**
```bash
python backend_full_crawl.py
```

2. **Launch the Frontend:**

- Option A: Open `index.html` in browser
- Option B: Serve frontend via local server:
```bash
python3 -m http.server 5500
```
Then go to: `http://localhost:5500/index.html`

---

## 🔍 Crawling Logic

- The server crawls internal links from the given root URL (up to 30 pages)
- Relative links are converted to absolute using `urljoin`
- Invalid links like `#`, `mailto:`, or `javascript:` are ignored
- Unique valid URLs are passed to `WebBaseLoader` for content extraction

---

## 🔗 API Endpoints

- `POST /upload_url`: Accepts JSON with `url` and `persona`, crawls and indexes content
- `POST /query`: Accepts a `query` and `history`, returns an LLM-generated answer
- `GET /new_session`: Generates a new session ID
- `POST /export_chat`: Exports chat to Excel
- `GET /health`: Health check

---

## 🧠 Sample Use Case (Amity University)

**Persona Example:**
```
You are an academic assistant trained to extract accurate information about Amity University Mohali based on their website. Do not hallucinate answers. If the content is unavailable, say so politely.
```

**Sample Questions:**
- What programs are offered at Amity University Mohali?
- How do I apply for B.Tech or MBA?
- Are scholarships available?
- What facilities does the campus offer?

---

## 🔐 Note

- Replace `your_groq_api_key_here` in `backend_full_crawl.py` with your actual [Groq API Key](https://console.groq.com/)

---

## 🤝 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain)
- [HuggingFace Transformers](https://huggingface.co/sentence-transformers)
- [Groq API](https://console.groq.com/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
