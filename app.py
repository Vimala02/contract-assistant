# from dotenv import load_dotenv
# load_dotenv()  # make sure Streamlit also sees OPENAI_API_KEY

import streamlit as st
from query_agent import answer_query, get_docs

st.title("Intelligent Contract Assistant — Demo")

q = st.text_input("Ask about contracts")
if st.button("Run") and q.strip():
    docs = get_docs(q,k=5)
    ans = answer_query(q)

    st.subheader("Answer")
    st.write(ans)

    st.subheader("Top retrieved snippets (provenance)")
    for d in docs[:5]:
        st.write(f"**Source**: {d.metadata.get('source_file', '-')}")
        st.write(d.page_content[:600] + "...")
