import argparse
import io
import os
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import date
import logging
import uuid

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text

# Konfigurasi
BASE_URL = "https://putusan3.mahkamahagung.go.id/search.html"
OUTPUT_DIR = "data/raw"
LOG_FILE = "logs/cleaning.log"
MIN_TEXT_COMPLETENESS = 0.8
NUM_DOCS = 30
KEYWORD = "Diversi"

# Setup logging
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Setup output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_args(argv=None):
    parser = argparse.ArgumentParser(description="Putusan Mahkamah Agung Scraper")
    parser.add_argument("-k", "--keyword", default=KEYWORD, help="Keyword for search")
    parser.add_argument("-n", "--num-docs", type=int, default=NUM_DOCS, help="Number of documents to scrape")
    return parser.parse_args(argv)

def open_page(link):
    count = 0
    while count < 3:
        try:
            response = requests.get(link, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, "lxml")
        except Exception as e:
            count += 1
            logging.error(f"Error opening page {link}: {str(e)}")
            time.sleep(5)
    logging.error(f"Failed to open page {link} after 3 attempts")
    return None

def get_pdf(url):
    try:
        file = urllib.request.urlopen(url)
        file_name = file.info().get_filename().replace("/", "_") if file.info().get_filename() else f"case_{uuid.uuid4().hex[:8]}.pdf"
        file_data = file.read()
        logging.info(f"Downloaded PDF: {file_name}")
        return io.BytesIO(file_data), file_name
    except Exception as e:
        logging.error(f"Error downloading PDF {url}: {str(e)}")
        return None, ""

def clean_text(text):
    try:
        original_length = len(text)
        # Bersihkan elemen umum
        text = re.sub(r'M a h ka m a h A g u n g R e p u blik In d o n esia\n*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Disclaimer\n*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Page \d+ of \d+', '', text)
        text = re.sub(r'© Mahkamah Agung.*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Kepaniteraan Mahkamah Agung.*?\n', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Email\s*:\s*kepaniteraan@mahkamahagung\.go\.id.*?\n', '', text, flags=re.IGNORECASE)
        
        # Normalisasi whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        logging.info(f"Cleaned text length: {len(text)}/{original_length} characters")
        return text, original_length
    except Exception as e:
        logging.error(f"Error cleaning text: {str(e)}")
        return text, len(text)

def validate_text(text, original_length):
    if not text:
        return False
    completeness = len(text) / original_length if original_length > 0 else 0
    has_keywords = any(keyword in text.lower() for keyword in ['menimbang', 'mengadili', 'putusan'])
    is_valid = completeness >= MIN_TEXT_COMPLETENESS and has_keywords
    logging.info(f"Text validation: completeness={completeness:.2%}, has_keywords={has_keywords}, valid={is_valid}")
    return is_valid

def extract_data(link, index):
    soup = open_page(link)
    if not soup:
        return None

    try:
        # Metadata
        table = soup.find("table", {"class": "table"})
        judul = table.find("h2").text.strip() if table and table.find("h2") else "Unknown"
        
        # PDF
        link_pdf = soup.find("a", href=re.compile(r"/pdf/"))
        if not link_pdf:
            logging.warning(f"No PDF link found for {link}")
            return None

        file_pdf, file_name_pdf = get_pdf(link_pdf["href"])
        if not file_pdf:
            return None

        text_pdf = extract_text(file_pdf)
        cleaned_text, original_length = clean_text(text_pdf)

        if not validate_text(cleaned_text, original_length):
            logging.warning(f"Text validation failed for {file_name_pdf}")
            return None

        output_file = os.path.join(OUTPUT_DIR, f"case_{index:03d}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
        logging.info(f"Saved cleaned text to {output_file}")

        return {
            "judul": judul,
            "link": link,
            "link_pdf": link_pdf["href"],
            "file_name_pdf": file_name_pdf
        }
    except Exception as e:
        logging.error(f"Error processing {link}: {str(e)}")
        return None

def run_process(keyword, page, num_docs, collected_docs):
    link = f"{BASE_URL}?q={keyword}&page={page}"
    soup = open_page(link)
    if not soup:
        return []

    links = soup.find_all("a", {"href": re.compile("/direktori/putusan")})
    results = []
    for link in links:
        if len(collected_docs) >= num_docs:
            break
        result = extract_data(link["href"], len(collected_docs) + 1)
        if result:
            results.append(result)
            collected_docs.append(result)
    return results

def main():
    args = get_args()
    keyword = args.keyword
    num_docs = args.num_docs
    logging.info(f"Starting scraping for keyword: {keyword}, target: {num_docs} documents")

    soup = open_page(f"{BASE_URL}?q={keyword}&page=1")
    if not soup:
        logging.error("Failed to access search page. Exiting.")
        return

    last_page = 1
    try:
        last_page = int(soup.find_all("a", {"class": "page-link"})[-1].get("data-ci-pagination-page"))
        logging.info(f"Found {last_page} pages of search results")
    except:
        logging.warning("Could not determine last page, defaulting to 1")

    collected_docs = []
    futures = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        for page in range(1, last_page + 1):
            if len(collected_docs) >= num_docs:
                break
            futures.append(executor.submit(run_process, keyword, page, num_docs, collected_docs))
        wait(futures)

    if collected_docs:
        df = pd.DataFrame(collected_docs)
        csv_file = f"{OUTPUT_DIR}/putusan_{keyword.lower()}_{date.today().strftime('%Y-%m-%d')}.csv"
        df.to_csv(csv_file, index=False)
        logging.info(f"Saved {len(collected_docs)} documents metadata to {csv_file}")

    logging.info(f"Completed: {len(collected_docs)}/{num_docs} documents processed successfully")

if __name__ == "__main__":
    main()
