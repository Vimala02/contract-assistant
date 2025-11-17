# from dotenv import load_dotenv
# load_dotenv()  # load OPENAI_API_KEY from .env

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

def get_docs(query: str, k: int = 10):
    """Simple helper to retrieve top-k docs from FAISS."""
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
