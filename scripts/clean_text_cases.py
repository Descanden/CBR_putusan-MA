# scripts/clean_text_cases.py
import os
import re

RAW_DIR = "data/raw"
LOG_PATH = "logs/cleaning.log"
os.makedirs("logs", exist_ok=True)

log = []

def clean_text(text):
    original_len = len(text)
    text = re.sub(r"[\r\t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[^a-zA-Z0-9\s.,;:\n-]", "", text)
    text = text.lower()
    cleaned_len = len(text)
    return text.strip(), original_len, cleaned_len

for filename in os.listdir(RAW_DIR):
    if filename.endswith(".txt"):
        file_path = os.path.join(RAW_DIR, filename)
        with open(file_path, encoding="utf-8") as f:
            text = f.read()
        cleaned_text, before, after = clean_text(text)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
        log.append(f"[{filename}] cleaned {before-after} chars, final size: {after} chars")

# Simpan log
with open(LOG_PATH, "w", encoding="utf-8") as f:
    for line in log:
        f.write(line + "\n")
print(f"📝 Log pembersihan tersimpan di {LOG_PATH}")
