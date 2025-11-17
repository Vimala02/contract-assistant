
import streamlit as st
from query_agent import answer_query, get_docs, get_vendors  # note: get_vendors added

st.set_page_config(page_title="Intelligent Contract Assistant", layout="wide")

st.title("Intelligent Contract Assistant — Demo")

# --- Sidebar: Vendor filter ---
st.sidebar.header("Filters")

# Get vendor list from vector store / metadata
vendors = get_vendors()  # this will return e.g. ["Vendor A", "Vendor B", "Vendor X", ...]
vendor_options = ["All vendors"] + vendors
selected_vendor = st.sidebar.selectbox("Filter by vendor", vendor_options)

st.sidebar.markdown("---")
st.sidebar.write("Tip: Try queries like:")
st.sidebar.write("- **Summarize the SLA terms**")
st.sidebar.write("- **When does Vendor X's contract auto-renew?**")
st.sidebar.write("- **Extract penalty clauses over $500**")

# --- Main area: Query box ---
q = st.text_input("Ask about contracts")

if st.button("Run") and q.strip():
    # Translate sidebar selection to vendor filter argument
    vendor_filter = None if selected_vendor == "All vendors" else selected_vendor

    # Use our helper to retrieve docs (filtered by vendor if chosen)
    docs = get_docs(q, k=5, vendor=vendor_filter)

    # Get final answer from agent
    ans = answer_query(q)

    st.subheader("Answer")
    st.write(ans)

    st.subheader("Top retrieved snippets (provenance)")
    if not docs:
        st.write("No documents found for this query and filter.")
    else:
        for d in docs[:5]:
            src = d.metadata.get("source_file", "-")
            vendor = d.metadata.get("vendor", "Unknown vendor")
            st.markdown(f"**Source**: `{src}` • **Vendor**: `{vendor}`")
            st.write(d.page_content[:600] + "...")
