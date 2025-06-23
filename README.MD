# Case-Based Reasoning on Indonesian Court Decisions  
An end-to-end pipeline for building a CBR system using court decisions from Mahkamah Agung Republik Indonesia.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Pipeline: Step-by-Step](#pipeline-step-by-step)
  - [Stage 1: Build Case Base](#stage-1-build-case-base)
- [License & Credits](#license--credits)

---

## Overview
This repository implements the first stage of a Case-Based Reasoning (CBR) system on Indonesian court rulings.

**Focus:**
- PDF corpus processing of court decisions from the official Supreme Court directory.
- Automatic cleaning and validation of raw court documents.
- Preparation of a reusable, high-quality case base for future CBR tasks.

### Domain:
**Perdata Perusahaan** (e.g., company civil disputes)

---

## Installation

First, set up your Python environment and install required packages:

```bash
# Clone the repository
git clone https://github.com/yourusername/CBR-Law-Cleaning.git
cd CBR-Law-Cleaning

# Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
