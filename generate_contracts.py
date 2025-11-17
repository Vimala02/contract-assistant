# generate_contracts.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import random, os
from datetime import datetime, timedelta

vendors = ["Vendor A","Vendor B","Vendor X","Vendor Y","Vendor Z"]
clauses = [
    ("Renewal","This agreement will auto-renew for 1 year unless either party provides 60 days written notice prior to renewal."),
    ("SLA","Service level: 99.5% uptime. Response time: critical 2h; major 4h; minor 24h."),
    ("Termination","Either party may terminate with 30 days notice for convenience. For breach, 7 day cure."),
    ("Penalty","Late delivery penalty: $600 per day up to $10,000."),
    ("Confidentiality","Both parties shall keep confidential all proprietary information for 3 years.")
]

os.makedirs("sample_contracts", exist_ok=True)
for i in range(1,8):
    vendor = random.choice(vendors)
    doc_num = f"CTR-{i:03d}"
    start = datetime.today() - timedelta(days=random.randint(0,800))
    renew_in = random.randint(30,365)
    c = canvas.Canvas(f"sample_contracts/{doc_num}.pdf", pagesize=A4)
    text = c.beginText(40, 800)
    text.textLine(f"Contract ID: {doc_num}")
    text.textLine(f"Vendor: {vendor}")
    text.textLine(f"Start Date: {start.strftime('%Y-%m-%d')}")
    text.textLine(f"Term: 12 months")
    text.textLine("")
    for _ in range(3):
        cl = random.choice(clauses)
        text.textLine(f"Clause: {cl[0]}")
        text.textLine(cl[1])
        text.textLine("")
    if random.random() > 0.5:
        renew_date = (start + timedelta(days=renew_in)).strftime("%Y-%m-%d")
        text.textLine(f"Auto-Renewal Date: {renew_date}")
    c.drawText(text)
    c.showPage()
    c.save()
print("Generated sample_contracts/*.pdf")
