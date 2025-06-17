import os
import requests
from bs4 import BeautifulSoup
from time import sleep

BASE_URL = "https://putusan3.mahkamahagung.go.id/search.html?q=Diversi&page={}"
SAVE_DIR = "data/source"
os.makedirs(SAVE_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0"
}

case_links = set()
page = 1

print("Mulai mencari putusan Diversi...")

# Loop sampai minimal 30 link ditemukan
while len(case_links) < 30:
    url = BASE_URL.format(page)
    print(f"Mengakses halaman ke-{page}...")

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
    except Exception as e:
        print(f"Gagal mengakses {url}: {e}")
        break

    soup = BeautifulSoup(res.text, "html.parser")
    found_links = 0

    for a in soup.select("a"):
        href = a.get("href", "")
        if "/putusan/" in href and "node" not in href:  # type: ignore
            full_url = f"https://putusan3.mahkamahagung.go.id{href}"
            if full_url not in case_links:
                case_links.add(full_url)
                found_links += 1

    print(f"Ditemukan {found_links} link baru (total: {len(case_links)})")

    if found_links == 0:
        print("Tidak ada link baru ditemukan, mungkin hasil sudah habis.")
        break

    page += 1
    sleep(2)

# Simpan HTML
print(f"Menyimpan {len(case_links)} dokumen HTML ke folder {SAVE_DIR}")
for idx, link in enumerate(sorted(case_links)):
    try:
        res = requests.get(link, headers=headers)
        res.raise_for_status()
        with open(f"{SAVE_DIR}/case_{idx+1:03d}.html", "w", encoding="utf-8") as f:
            f.write(res.text)
        print(f"Sukses simpan: case_{idx+1:03d}.html")
        sleep(2)
    except Exception as e:
        print(f"Gagal unduh {link}: {e}")

print("Selesai. Total dokumen yang disimpan:", len(case_links))
