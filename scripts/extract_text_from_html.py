# scripts/extract_text_from_html.py
import os
from bs4 import BeautifulSoup

SOURCE_DIR = "data/source"
RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

def extract_text(html_file):
    with open(html_file, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    content_div = soup.find("div", {"id": "content"})
    if content_div:
        return content_div.get_text(separator="\n")
    return ""

for filename in os.listdir(SOURCE_DIR):
    if filename.endswith(".html"):
        full_path = os.path.join(SOURCE_DIR, filename)
        text = extract_text(full_path)
        output_path = os.path.join(RAW_DIR, filename.replace(".html", ".txt"))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✔ Ekstraksi: {filename}")
