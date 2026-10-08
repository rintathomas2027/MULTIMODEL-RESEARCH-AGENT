import os
import math
import re
from pathlib import Path
from django.conf import settings
import google.generativeai as genai

# Configure Gemini API if available
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

if os.getenv('VERCEL', '0') == '1' or 'VERCEL_ENV' in os.environ:
    CHROMA_DB_DIR = '/tmp/chroma_db'
else:
    CHROMA_DB_DIR = os.path.join(settings.BASE_DIR, 'chroma_db')
os.makedirs(CHROMA_DB_DIR, exist_ok=True)

try:
    import chromadb
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
except Exception as e:
    print(f"ChromaDB persistent client init warning: {e}")
    chroma_client = None

def get_or_create_collection(collection_name="scholarpulse_docs"):
    if chroma_client:
        return chroma_client.get_or_create_collection(name=collection_name)
    return None

def generate_embedding(text):
    """
    Generate vector embeddings using Gemini API (embedding-001 or text-embedding-004).
    If API fails or not set, returns None to trigger fallback search.
    """
    if not GEMINI_API_KEY:
        return None

    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        try:
            # Fallback to older embedding model name if needed
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as ex:
            print(f"Gemini Embedding Warning: {ex}")
            return None

def store_document_chunks(doc_id, chunks):
    """
    Store text chunks in ChromaDB vector store.
    """
    if not chunks:
        return 0

    collection = get_or_create_collection()
    if not collection:
        return len(chunks)

    ids = [f"doc_{doc_id}_chunk_{c['index']}" for c in chunks]
    documents = [c['text'] for c in chunks]
    metadatas = [{'doc_id': str(doc_id), 'chunk_index': c['index']} for c in chunks]

    # Attempt to generate embeddings
    embeddings = []
    for c in chunks:
        emb = generate_embedding(c['text'][:1000])
        if emb:
            embeddings.append(emb)

    try:
        if len(embeddings) == len(chunks):
            collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
        else:
            # Add without custom embeddings, letting Chroma handle or fallback
            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
    except Exception as e:
        print(f"Error adding chunks to ChromaDB: {e}")

    return len(chunks)

def delete_document_chunks(doc_id):
    """
    Remove vectors corresponding to doc_id from ChromaDB.
    """
    try:
        collection = get_or_create_collection()
        if collection:
            collection.delete(where={'doc_id': str(doc_id)})
    except Exception as e:
        print(f"Error deleting doc {doc_id} from ChromaDB: {e}")

def retrieve_similar_chunks(doc_id, query, top_k=4):
    """
    Retrieve top_k most relevant text chunks for a query from ChromaDB.
    Falls back to TF-IDF text relevance scoring if vector search is unavailable.
    """
    collection = get_or_create_collection()
    retrieved_text_chunks = []

    if collection:
        try:
            query_emb = generate_embedding(query)
            if query_emb:
                results = collection.query(
                    query_embeddings=[query_emb],
                    n_results=top_k,
                    where={'doc_id': str(doc_id)}
                )
            else:
                results = collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    where={'doc_id': str(doc_id)}
                )

            if results and 'documents' in results and results['documents']:
                for doc_list in results['documents']:
                    retrieved_text_chunks.extend(doc_list)
        except Exception as e:
            print(f"ChromaDB retrieval fallback: {e}")

    return retrieved_text_chunks

def tfidf_fallback_search(full_text, query, top_k=4):
    """
    TF-IDF keyword matching fallback if vector store is empty.
    """
    if not full_text:
        return []

    lines = [line.strip() for line in full_text.split('\n') if len(line.strip()) > 30]
    if not lines:
        lines = [full_text[i:i+500] for i in range(0, len(full_text), 450)]

    query_words = set(re.findall(r'\w+', query.lower()))
    scored_lines = []

    for line in lines:
        line_words = set(re.findall(r'\w+', line.lower()))
        overlap = len(query_words.intersection(line_words))
        if overlap > 0:
            scored_lines.append((overlap, line))

    scored_lines.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored_lines[:top_k]]
