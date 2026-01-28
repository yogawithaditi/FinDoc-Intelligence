#!/usr/bin/env python3
"""
FinDoc Intelligence - Streamlit App
====================================

Modern web interface for financial document analysis.

Features:
- Document upload (PDF, images)
- Text extraction (OCR + PDF)
- Chat interface
- Conversation history
- Document management

Author: Built for FinDoc Intelligence project
"""

import streamlit as st
from pathlib import Path
import uuid
from datetime import datetime
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))
sys.path.append(str(Path(__file__).parent / "utils"))

from src.document_processor import DocumentProcessor
from utils.db_manager import get_db


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FinDoc Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

def init_session_state():
    """Initialize session state variables."""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if 'processor' not in st.session_state:
        st.session_state.processor = DocumentProcessor()
    
    if 'db' not in st.session_state:
        st.session_state.db = get_db()
    
    if 'current_document' not in st.session_state:
        st.session_state.current_document = None
    
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = None
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def save_uploaded_file(uploaded_file) -> Path:
    """
    Save uploaded file to disk.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Path to saved file
    """
    upload_dir = Path("data/uploaded")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = upload_dir / uploaded_file.name
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path


def process_uploaded_document(file_path: Path):
    """
    Process uploaded document and update session state.
    
    Args:
        file_path: Path to the uploaded file
    """
    with st.spinner("🔄 Processing document..."):
        # Process document
        result = st.session_state.processor.process_document(file_path)
        
        if result['success']:
            # Save to session state
            st.session_state.current_document = result['file_name']
            st.session_state.extracted_text = result['text']
            
            # Save to database
            doc_id = st.session_state.db.save_document_metadata(
                filename=result['file_name'],
                file_type=result['file_type'],
                text_length=len(result['text']),
                document_type=None  # Will be classified in Week 4
            )
            
            # Save processed text
            st.session_state.processor.save_extracted_text(
                result, 
                Path("data/processed")
            )
            
            return True, result
        else:
            return False, result


# ============================================================
# MAIN APP
# ============================================================

def main():
    """Main application logic."""
    
    # Initialize session state
    init_session_state()
    
    # Header
    st.markdown('<div class="main-header">🏦 FinDoc Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Financial Document Analysis</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📄 Document Upload")
        
        uploaded_file = st.file_uploader(
            "Upload financial document",
            type=['pdf', 'png', 'jpg', 'jpeg', 'tiff'],
            help="Supports PDFs, scanned images, and photos"
        )
        
        if uploaded_file:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            if st.button("🚀 Process Document", type="primary"):
                # Save file
                file_path = save_uploaded_file(uploaded_file)
                
                # Process document
                success, result = process_uploaded_document(file_path)
                
                if success:
                    st.success("✅ Document processed successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ Error: {result['error']}")
        
        st.divider()
        
        # Document history
        st.header("📚 Recent Documents")
        docs = st.session_state.db.get_uploaded_documents(limit=5)
        
        if docs:
            for doc in docs:
                st.text(f"📄 {doc['filename'][:30]}...")
        else:
            st.info("No documents uploaded yet")
        
        st.divider()
        
        # Session info
        st.header("ℹ️ Session Info")
        st.caption(f"Session ID: {st.session_state.session_id[:8]}...")
        
        if st.button("🗑️ Clear History"):
            st.session_state.db.clear_session_history(st.session_state.session_id)
            st.session_state.chat_history = []
            st.success("History cleared!")
            st.rerun()
    
    # Main content area
    if st.session_state.current_document is None:
        # Welcome screen
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>📄 Document Processing</h3>
                <p>Upload PDFs, scanned images, or photos of financial documents</p>
                <ul>
                    <li>PDF text extraction</li>
                    <li>OCR for images</li>
                    <li>Multi-page support</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>🔍 Data Extraction</h3>
                <p>Automatically extract structured financial data</p>
                <ul>
                    <li>Credit scores & ratings</li>
                    <li>Financial metrics</li>
                    <li>Company information</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>💬 Q&A Assistant</h3>
                <p>Ask questions about your documents</p>
                <ul>
                    <li>RAG-powered responses</li>
                    <li>Source citations</li>
                    <li>Conversation history</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Instructions
        st.markdown("""
        ### 🚀 Getting Started
        
        1. **Upload a document** using the sidebar
        2. **Click "Process Document"** to extract text
        3. **Ask questions** about the document in the chat
        
        ### 📊 Supported Document Types
        
        - **Credit Reports** (Creditsafe, D&B, Experian)
        - **Financial Statements** (Balance Sheets, Income Statements)
        - **Rating Reports** (S&P, Moody's, Fitch)
        - **Company Documents** (Annual Reports, Prospectuses)
        """)
    
    else:
        # Document loaded - show analysis interface
        st.header(f"📄 Current Document: {st.session_state.current_document}")
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["💬 Chat", "📝 Extracted Text", "📊 Analytics"])
        
        with tab1:
            st.subheader("Ask questions about the document")
            
            # Chat interface
            user_input = st.text_input(
                "Your question:",
                placeholder="What's the credit score? What's the company's revenue?",
                key="user_input"
            )
            
            if st.button("Send", type="primary"):
                if user_input:
                    # For now, simple response (Week 3 will add RAG)
                    response = f"📝 I received your question: '{user_input}'\n\n"
                    response += "🚧 RAG system coming in Week 3! For now, I can show you the extracted text."
                    
                    # Save to chat history
                    st.session_state.chat_history.append({
                        'user': user_input,
                        'assistant': response,
                        'timestamp': datetime.now()
                    })
                    
                    # Save to database
                    st.session_state.db.save_conversation(
                        session_id=st.session_state.session_id,
                        user_message=user_input,
                        assistant_message=response,
                        document_name=st.session_state.current_document
                    )
                    
                    st.rerun()
            
            # Display chat history
            if st.session_state.chat_history:
                st.divider()
                for msg in st.session_state.chat_history:
                    st.markdown(f"**You:** {msg['user']}")
                    st.markdown(f"**Assistant:** {msg['assistant']}")
                    st.caption(f"_{msg['timestamp'].strftime('%H:%M:%S')}_")
                    st.divider()
        
        with tab2:
            st.subheader("Extracted Text")
            
            if st.session_state.extracted_text:
                # Show stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Characters", len(st.session_state.extracted_text))
                with col2:
                    word_count = len(st.session_state.extracted_text.split())
                    st.metric("Words", word_count)
                with col3:
                    line_count = len(st.session_state.extracted_text.split('\n'))
                    st.metric("Lines", line_count)
                
                st.divider()
                
                # Show text in expandable section
                with st.expander("📄 View Full Text", expanded=False):
                    st.text_area(
                        "Extracted text:",
                        value=st.session_state.extracted_text,
                        height=400,
                        disabled=True
                    )
                
                # Show preview
                st.subheader("Preview (first 1000 characters)")
                st.text(st.session_state.extracted_text[:1000] + "...")
            else:
                st.info("No text extracted yet")
        
        with tab3:
            st.subheader("Document Analytics")
            st.info("📊 Analytics features coming in Week 2-4!")
            st.markdown("""
            **Coming soon:**
            - Extracted financial metrics
            - Data visualizations
            - Comparison charts
            - SQL queries on financial data
            """)


# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":
    main()