# Case-Based Reasoning on Civil Court Decisions (PMH)
An end-to-end pipeline for building a Case-Based Reasoning (CBR) system using Supreme Court decisions in civil law—specifically *Perbuatan Melawan Hukum* (Unlawful Acts), comparing the performance of **TF-IDF + Cosine Similarity** and **TF-IDF + SVM** approaches.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Running the Pipeline](#running-the-pipeline)
- [Evaluation Results](#evaluation-results)
- [License & Credits](#license--credits)

---

## Overview

This project implements a *Case-Based Reasoning* system to support legal analysis and recommendation based on previous court cases. The pipeline includes five main stages: document scraping, information extraction, case representation, case retrieval, and solution evaluation — **all integrated into a single notebook file**: `casebase_build.ipynb`.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Descanden/CBR_putusan-MA.git
cd CBR_putusan-MA
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv

# For Windows
venv\Scripts\activate

# If PowerShell policy error:
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# For macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` is still empty, you can generate it automatically:
```bash
pip install pipreqs
pipreqs . --force
```

---

## Project Structure

```bash
CBR_putusan-MA/
├── data/
│   ├── raw/                     # Cleaned court decision texts
│   ├── processed/               # Metadata, features, vector representations
│   ├── results/                 # Predicted solutions
│   └── eval/                    # Evaluation results and visualizations
├── logs/                        # Text cleaning logs
├── PMH_PDF/                     # Raw Supreme Court PDF files
├── casebase_build.ipynb        # Complete CBR pipeline notebook
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies
```

---

## Running the Pipeline

All stages of the project are executed within the notebook file: `casebase_build.ipynb`.

### ❐ Pipeline Stages:
1. **Stage 1 – Case Base Construction**
   - Read PDF files from `PMH_PDF/`
   - Extract and clean text content
   - Save cleaned text to `data/raw/`
   - Write logs to `logs/cleaning.log`

2. **Stage 2 – Case Representation**
   - Extract metadata: case number, date, parties, legal articles
   - Generate case fact summaries
   - Build features: text length, Bag-of-Words, QA-pairs

3. **Stage 3 – Case Retrieval**
   - Convert text into TF-IDF vectors
   - Build retrieval models:
     - TF-IDF + Cosine Similarity
     - TF-IDF + SVM classifier

4. **Stage 4 – Solution Reuse**
   - Retrieve the most similar past case
   - Reuse the previous court verdict as prediction

5. **Stage 5 – Evaluation**
   - Evaluate model predictions using:
     - Accuracy, Precision, Recall, F1-score
   - Save evaluation outputs to `data/eval/`

### ❐ Run via:
```bash
jupyter notebook casebase_build.ipynb
```

---

## Evaluation Results

### TF-IDF + Cosine Similarity

| Metric     | Score |
|------------|-------|
| Accuracy   | 0.90  |
| Precision  | 1.00  |
| Recall     | 0.90  |
| F1-Score   | 0.947 |


---

### TF-IDF + SVM

| Metric     | Score |
|------------|-------|
| Accuracy   | 0.70  |
| Precision  | 1.00  |
| Recall     | 0.70  |
| F1-Score   | 0.823 |


---

## License & Credits

This project was developed as part of the course assignment **Computer Reasoning – 6th Semester**, Universitas Muhammadiyah Malang.

**Team Members:**
- Rofiq Samanhudi (202210370311260)  
- Muhammad Ikbar Ananda Sulistio (202210370311236)

---
