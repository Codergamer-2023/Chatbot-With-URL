from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from groq import Groq
import os
import pandas as pd
from io import BytesIO

app = Flask(__name__)
CORS(app)

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
groq_client = Groq(api_key="")  
vector_db = None
system_persona = None

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def crawl_website(start_url, max_links=30):
    visited = set()
    to_visit = [start_url]
    domain = urlparse(start_url).netloc

    while to_visit and len(visited) < max_links:
        url = to_visit.pop(0)
        if url in visited:
            continue
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                continue
            visited.add(url)

            soup = BeautifulSoup(response.text, 'html.parser')
            for link_tag in soup.find_all('a', href=True):
                href = link_tag['href']
                full_url = urljoin(url, href)
                if urlparse(full_url).netloc == domain and full_url not in visited:
                    to_visit.append(full_url)
        except Exception as e:
            print(f"Failed to crawl {url}: {e}")

    return list(visited)


@app.route('/upload_url', methods=['POST'])
def upload_url():
    global vector_db, system_persona
    try:
        data = request.get_json()
        if 'url' not in data or 'persona' not in data:
            return jsonify({'error': 'URL and persona are required'}), 400
        
        url = data['url']
        persona = data['persona']
        all_urls = crawl_website(url, max_links=30)

        
        loader = WebBaseLoader(web_paths=[all_urls])
        web_documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        documents = text_splitter.split_documents(web_documents)
        
        vector_db = Chroma.from_documents(documents, embedding_model)
        system_persona = persona
        
        return jsonify({
            'message': 'Web page processed successfully',
            'url': url,
            'chunk_count': len(documents)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/query', methods=['POST'])
def query():
    try:
        if vector_db is None or system_persona is None:
            return jsonify({'error': 'No URL or persona has been provided yet', 'answer': ''}), 400
            
        data = request.get_json()
        if not data or 'query' not in data or 'history' not in data:
            return jsonify({'error': 'Query and history are required', 'answer': ''}), 400
            
        query_text = data['query']
        chat_history = data['history']
        
        results = vector_db.similarity_search(query_text, k=5)
        seen = set()
        unique_results = []
        for doc in results:
            content = doc.page_content
            if content not in seen:
                seen.add(content)
                unique_results.append(doc)
        
        context = "\n\n".join([doc.page_content for doc in unique_results])
        
        messages = [{
            "role": "system",
            "content": system_persona
        }]
        
        for chat in chat_history:
            messages.append({"role": "user", "content": chat['user']})
            messages.append({"role": "assistant", "content": chat['bot']})
        
        messages.append({
            "role": "user",
            "content": f"Using the following context, answer the question:\n\n{context}\n\nQ: {query_text}"
        })
        
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_completion_tokens=1024
        )
        
        return jsonify({
            'answer': response.choices[0].message.content,
            'query': query_text
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e), 'answer': ''}), 500


import uuid
@app.route('/new_session', methods=['GET'])
def new_session():
    """Generates a new session ID"""
    return jsonify({"session_id": str(uuid.uuid4())}), 200


@app.route('/export_chat', methods=['POST'])
def export_chat():
    try:
        data = request.get_json()
        if not data or 'history' not in data:
            return jsonify({'error': 'Chat history is required'}), 400
            
        chat_history = data['history']
        df = pd.DataFrame(chat_history, columns=['user', 'bot'])
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='chat_history.xlsx'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
