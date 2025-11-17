### Project Structure

contract_assistant/
│
├── app.py                   # Streamlit UI
├── query_agent.py           # Query handler + agent tools
├── ingest_index.py          # PDF → chunks → embeddings → FAISS index
├── agent_tools.py           # SLA, renewal, penalty extraction logic
├── generate_contracts.py    # Synthetic contract generator (optional)
│
├── sample_contracts/        # 5–10 dummy PDF contracts
├── faiss_index/             # Generated FAISS vector store
│
├── requirements.txt
├── .gitignore
└── README.md                # This file

### Architecture

PDF Contracts → PDF Loader → Text Chunking
     ↓
Embeddings (HuggingFace MiniLM)
     ↓
FAISS Vector Store
     ↓
Retriever
     ↓
Agent Tools (SLA, Renewal, Penalties)
     ↓
LLM (OpenAI or Local)
     ↓
Streamlit UI


### Setup

Setup Instructions
1️⃣ Clone project
git clone https://github.com/<username>/contract-assistant.git
cd contract-assistant

2️⃣ Create virtual environment
python -m venv .pyven
.\.pyven\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Build FAISS index
python ingest_index.py


### Expected output:

Loaded docs: 7
Saved index to faiss_index

5️⃣ Run the Streamlit App
streamlit run app.py


### Your UI starts at:
http://localhost:8501


### 🎤 Sample Queries

Try these in the UI:

“Summarize SLA terms for all vendors.”
“When does Vendor X's contract auto-renew?”
“Extract penalty clauses over $500.”
“Which vendors have termination period < 30 days?”