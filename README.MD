Case-Based Reasoning for Supreme Court Decisions Analysis
This repository contains a Python-based pipeline for analyzing Indonesian Supreme Court (Mahkamah Agung) civil case decisions (Perbuatan Melawan Hukum - PMH) using Case-Based Reasoning (CBR). The pipeline implements two approaches: TF-IDF + Cosine Similarity and TF-IDF + SVM to retrieve and predict solutions based on past court decisions.
GitHub Repository: https://github.com/Descanden/CBR_putusan-MA.git
Table of Contents

Project Overview
Requirements
Installation
Directory Structure
How to Run the Pipeline
Example Commands
Output Files
Contributors

Project Overview
The pipeline consists of five stages:

Case Base Building: Extracts and cleans text from PDF court decisions.
Case Representation: Extracts metadata and engineers features for structured data.
Case Retrieval: Retrieves similar cases using TF-IDF with Cosine Similarity or SVM.
Solution Reuse: Predicts solutions based on retrieved cases.
Model Evaluation: Evaluates the performance of both approaches.

The dataset includes 70 PMH court decisions, processed into a structured format for CBR analysis.
Requirements

Python 3.12 or higher
Required Python libraries are listed in requirements.txt.

Example requirements.txt
pdfminer.six==20231228
pandas==2.2.2
scikit-learn==1.5.1
joblib==1.4.2
matplotlib==3.9.2

Installation

Clone the repository:
git clone https://github.com/Descanden/CBR_putusan-MA.git
cd CBR_putusan-MA


Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:
pip install -r requirements.txt


Ensure the PMH_PDF/ directory contains PDF files of court decisions to be processed.


Directory Structure
CBR_putusan-MA/
├── PMH_PDF/                    # Input PDF files
├── data/
│   ├── raw/                    # Raw extracted text
│   ├── processed/              # Processed metadata and features
│   ├── eval/                   # Evaluation queries and results
│   ├── results/                # Prediction outputs
├── logs/                       # Log files
├── casebase_build.ipynb        # Main pipeline notebook
├── requirements.txt            # Dependencies
└── README.md                   # This file

How to Run the Pipeline
The entire pipeline is implemented in the Jupyter notebook casebase_build.ipynb. Follow these steps to run it end-to-end:

Prepare Input Data:

Place PDF court decision files in the PMH_PDF/ directory.
Ensure the directory structure is set up as described above.


Run the Notebook:

Open casebase_build.ipynb in Jupyter Notebook or JupyterLab:jupyter notebook


Execute all cells sequentially to perform the following:
Stage 1: Extract and clean text from PDFs, saving to data/raw/.
Stage 2: Extract metadata and features, saving to data/processed/.
Stage 3: Train retrieval models and save to 03_retrieval_model.pkl and 03_vectorizer.pkl.
Stage 4: Predict solutions for test queries, saving to data/results/.
Stage 5: Evaluate model performance, saving metrics and visualizations to data/eval/.




Alternative: Run Specific Stages:

You can execute individual cells or sections of the notebook to run specific stages (e.g., only Stage 3 for retrieval).



Example Commands

To start Jupyter Notebook:
jupyter notebook


To install dependencies (if not done yet):
pip install -r requirements.txt


Example of expected output after running the notebook:
[SUKSES] Tahap 5 - Evaluasi Model selesai
- Hasil evaluasi retrieval disimpan di: data/eval/retrieval_metrics.csv
- Hasil evaluasi prediksi disimpan di : data/eval/prediction_metrics.csv
- Visualisasi disimpan di             : data/eval/performance_comparison.png
- Error cosine disimpan di           : data/eval/error_cases_cosine.json
- Error svm disimpan di              : data/eval/error_cases_svm.json



Output Files
After running the pipeline, the following files are generated:

data/raw/*.txt: Cleaned text from PDFs.
data/processed/cases_extracted.csv: Extracted metadata in CSV format.
data/processed/cases_extracted.json: Extracted metadata in JSON format.
data/processed/features_*.json: Engineered features (length, BoW, QA pairs).
data/eval/queries.json: Test queries for evaluation.
data/results/predictions_cosine.csv: Predictions using Cosine Similarity.
data/results/predictions_svm.csv: Predictions using SVM.
data/eval/retrieval_metrics.csv: Retrieval performance metrics.
data/eval/prediction_metrics.csv: Prediction performance metrics.
data/eval/performance_comparison.png: Visualization of model performance.
data/eval/error_cases_*.json: Error analysis for both approaches.
logs/cleaning.log: Log of text cleaning process.
03_retrieval_model.pkl: Trained SVM model.
03_vectorizer.pkl: TF-IDF vectorizer.

Contributors

Rofiq Samanhudi (202210370311260)
Muhammad Ikbar Ananda Sulistio (202210370311236)

For questions or issues, please open an issue on the GitHub repository.