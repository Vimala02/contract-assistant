from dotenv import load_dotenv
load_dotenv()  # loads OPENAI_API_KEY from .env

from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI

from dateutil import parser as dateparser
import re
import json

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)

def summarize_sla(texts):
    prompt = """
You are a contracts analyst. Summarize the key SLA items from the text below as 3-5 concise bullets. 
If nothing found, return an empty list.

Text:
{context}

Output as JSON: {{
  "sla_summary": ["bullet 1", "bullet 2"]
}}
Return ONLY valid JSON.
"""
    context = "\n\n".join(texts)
    raw = llm.invoke(prompt.format(context=context))
    try:
        return json.loads(raw)
    except Exception:
        # If model returns something slightly off, just return raw text
        return raw


def extract_clauses_by_keyword(texts, keyword):
    combined = "\n\n".join(texts)
    matches = []
    for m in re.finditer(
        r"([^\n\.]*" + re.escape(keyword) + r"[^\n\.]*[\.]?)", combined, flags=re.I
    ):
        matches.append(m.group(0).strip())

    if not matches:
        prompt = (
            f"Extract any clause paragraphs related to '{keyword}' from the text "
            f"below. Return a JSON array of strings.\n\n{combined}"
        )
        res = llm.invoke(prompt)
        return res

    return matches


def extract_penalties_over_threshold(texts, threshold=500):
    combined = "\n\n".join(texts)
    amounts = []
    for m in re.finditer(r"[\$£€]\s?\d{1,3}(?:,\d{3})*(?:\.\d+)?", combined):
        amt_text = m.group(0)
        num = float(re.sub(r"[^0-9.]", "", amt_text))
        if num > threshold:
            start = max(0, m.start() - 80)
            end = min(len(combined), m.end() + 80)
            snippet = combined[start:end]
            amounts.append(
                {"amount": num, "currency": amt_text[0], "snippet": snippet}
            )
    return amounts
