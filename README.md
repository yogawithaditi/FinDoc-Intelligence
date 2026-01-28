# FinDoc Intelligence 🏦

**AI-Powered Financial Document Analysis System**

Process credit reports, financial statements, and company documents using ML classification and RAG-based question answering.

---

## 🎯 What This Does

1. **Upload** PDFs, scanned images, screenshots, or photos of financial documents
2. **Extract** structured data (credit scores, revenue, debt ratios, company info)
3. **Classify** document types using ML (Credit Report, Balance Sheet, Income Statement, Rating Report)
4. **Query** documents intelligently using RAG (ask questions, get answers)

---

## 📁 Project Structure

```
FinDoc-Intelligence/
├── src/                          # Source code
│   ├── document_processor.py    # PDF/Image text extraction + OCR
│   ├── data_extractor.py        # Structured data extraction (entities, amounts, dates)
│   ├── classifier.py            # ML document type classifier
│   └── rag_engine.py            # RAG system (vector DB + Q&A)
│
├── data/
│   ├── raw/                     # Uploaded documents (original)
│   ├── processed/               # Extracted text & structured data
│   └── sample_docs/             # Sample financial documents for testing
│
├── models/                      # Trained ML models & embeddings
├── outputs/                     # Query results & reports
├── tests/                       # Unit tests
│
├── requirements.txt             # Python dependencies (install as needed)
├── config.yaml                  # Configuration file
└── main.py                      # Main application entry point
```

---

## 🛠️ Tech Stack (Open Source)

- **Python 3.12** - Core language
- **PyPDF2 / pdfplumber** - PDF text extraction
- **Pillow + pytesseract** - OCR (Optical Character Recognition) for scanned images
- **scikit-learn** - ML classification models
- **sentence-transformers** - Text embeddings for RAG
- **ChromaDB / FAISS** - Vector database for document retrieval
- **Ollama + Llama** - Local LLM for question answering
- **Streamlit** - Simple web interface (optional)

---

## 🚀 Installation

We'll install dependencies **as needed** throughout development.

```bash
# Create virtual environment (when we start coding)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (we'll add these gradually)
pip install -r requirements.txt
```

---

## 📊 Sample Document Types We Handle

### 1. Credit Reports (Creditsafe/D&B style)
- Company name, registration number
- Credit score, credit limit
- Payment history, trade references

### 2. Financial Statements
- Balance sheets (assets, liabilities, equity)
- Income statements (revenue, expenses, profit)
- Key financial ratios

### 3. Rating Reports (S&P style)
- Credit ratings (AAA, BB+, etc.)
- Outlook (stable, positive, negative)
- Risk metrics

---

## 🎓 Learning Outcomes

By building this project, you'll understand:

- **RAG (Retrieval Augmented Generation)** - How to make LLMs answer questions from YOUR documents
- **ML Classification** - Training models to categorize documents
- **Data Extraction** - Pulling structured data from unstructured text
- **OCR** - Converting images to text
- **Vector Databases** - Storing and searching document embeddings
- **End-to-end ML Pipeline** - From raw data to production system

---

## 📝 Development Timeline (4 Weeks)

**Week 1:** Document Processing (OCR, PDF extraction)  
**Week 2:** Data Extraction + ML Classification  
**Week 3:** RAG System (Vector DB, Embeddings, Q&A)  
**Week 4:** Testing, Polish, Demo Interface

---

## 👨‍💻 Author

Built with domain expertise from S&P Global financial data research background.

**Skills Demonstrated:**
- Financial data domain knowledge
- ML/AI engineering
- Data pipeline development
- End-to-end system design

---

## 📄 License

MIT License - Feel free to use for learning and portfolio purposes.
