import streamlit as st
from src.crawler import WebsiteCrawler
from src.processor import TextProcessor
from src.vector_store import VectorStore
from src.generator import GeminiGenerator
import time

# Page Config
st.set_page_config(page_title="RAG Website Chatbot", layout="wide")

# Initialize Session State
if "vector_store" not in st.session_state:
    st.session_state.vector_store = VectorStore()
if "processor" not in st.session_state:
    st.session_state.processor = TextProcessor()
if "generator" not in st.session_state:
    try:
        st.session_state.generator = GeminiGenerator()
        st.session_state.api_active = True
    except Exception as e:
        st.error(f"Failed to initialize Gemini: {e}")
        st.session_state.api_active = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "website_processed" not in st.session_state:
    st.session_state.website_processed = False

# Sidebar: Inputs
with st.sidebar:
    st.header("Configuration")
    url_input = st.text_input("Enter Website URL", placeholder="https://example.com")
    
    if st.button("Process Website"):
        if not url_input:
            st.warning("Please enter a URL.")
        elif not st.session_state.api_active:
            st.error("API not active. Check .env file.")
        else:
            with st.status("Processing website...", expanded=True) as status:
                st.write("🕷️ Crawling website...")
                crawler = WebsiteCrawler()
                raw_text = crawler.get_content(url_input)
                
                if raw_text:
                    st.write("✂️ Chunking text...")
                    chunks = st.session_state.processor.chunk_text(raw_text)
                    st.write(f"Found {len(chunks)} chunks.")
                    
                    st.write("🧠 Generating embeddings...")
                    embeddings = st.session_state.processor.get_embeddings(chunks)
                    
                    st.write("💾 Storing in Vector DB...")
                    st.session_state.vector_store.clear() # Clear old data
                    st.session_state.vector_store.add_documents(chunks, embeddings)
                    
                    st.session_state.website_processed = True
                    status.update(label="Website Processed Successfully!", state="complete", expanded=False)
                else:
                    status.update(label="Failed to crawl website.", state="error")

# Main Chat Interface
st.title("🤖 Website RAG Chatbot")
st.caption("Powered by Gemini 1.5 Flash & ChromaDB")

# Display Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question about the website content..."):
    if not st.session_state.website_processed:
        st.error("Please process a website first!")
    else:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # 1. Embed query
                query_embedding = st.session_state.processor.get_embeddings([prompt])[0]
                
                # 2. Retrieve relevant chunks
                relevant_docs = st.session_state.vector_store.query(query_embedding)
                context_text = "\n\n".join(relevant_docs)
                
                # 3. Generate answer
                response = st.session_state.generator.generate_answer(context_text, prompt)
                
                st.markdown(response)
                
                # Add assistant message to history
                st.session_state.chat_history.append({"role": "assistant", "content": response})

                # Debug: Show retrieved context (Optional, good for demo)
                with st.expander("View Retrieved Context"):
                    st.text(context_text)