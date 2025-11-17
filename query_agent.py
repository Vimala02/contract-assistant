# from dotenv import load_dotenv
# load_dotenv()  # load OPENAI_API_KEY from .env

import re
from typing import List, Optional


from langchain_community.vectorstores import FAISS
#from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAI     # LLM
from langchain_huggingface import HuggingFaceEmbeddings

from agent_tools import (
    summarize_sla,
    extract_clauses_by_keyword,
    extract_penalties_over_threshold,
)

#emb = OpenAIEmbeddings()  # uses OPENAI_API_KEY if you have
emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vs = FAISS.load_local("faiss_index", embeddings=emb,allow_dangerous_deserialization=True)

def get_vendors() -> List[str]:
    """
    Scan documents for vendor names from metadata.
    Fallback: try to parse from text line 'Vendor: <name>'.
    """
    vendors = set()

    # FAISS docstore holds documents in vs.docstore._dict
    for doc in vs.docstore._dict.values():
        meta_vendor = doc.metadata.get("vendor")
        if meta_vendor:
            vendors.add(meta_vendor)
            continue

        # fallback: regex on content like 'Vendor: Vendor X'
        m = re.search(r"Vendor:\s*([A-Za-z0-9\s]+)", doc.page_content)
        if m:
            vendors.add(m.group(1).strip())

    return sorted(vendors)

def get_docs(query: str, k: int = 5, vendor: Optional[str] = None):
    """
    Retrieve top-k documents for query, optionally filtered by vendor metadata.
    """
    if vendor:
        # if you stored vendor in metadata at indexing time:
        return vs.similarity_search(query, k=k, filter={"vendor": vendor})

    # no vendor filter
    return vs.similarity_search(query, k=k)

llm = OpenAI(temperature=0, model_name="gpt-4o")


def answer_query(query: str):
    #docs = retriever.get_relevant_documents(query)
    docs = get_docs(query,k=10)
    snippets = [d.page_content for d in docs[:6]]
    q = query.lower()

    if "sla" in q and "summarize" in q:
        return summarize_sla(snippets)

    if "renew" in q:
        return extract_clauses_by_keyword(snippets, "renew")

    if "penalty" in q or "over" in q:
        return extract_penalties_over_threshold(snippets, 500)

    context = "\n\n".join(snippets[:4])
    prompt = (
        "Using the context below, answer the question concisely and cite source filenames.\n\n"
        f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
    )
    return llm.invoke(prompt)


if __name__ == "__main__":
    q = input("Ask: ")
    print(answer_query(q))
