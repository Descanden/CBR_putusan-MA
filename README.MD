# Case-Based Reasoning pada Putusan Perdata PMH
Sebuah pipeline end-to-end untuk membangun sistem Case-Based Reasoning (CBR) menggunakan dokumen putusan Mahkamah Agung dalam perkara Perdata – Perbuatan Melawan Hukum (PMH), dengan pembandingan pendekatan **TF-IDF + Cosine Similarity** dan **TF-IDF + SVM**.

## Daftar Isi
- [Overview](#overview)
- [Instalasi](#instalasi)
- [Struktur Proyek](#struktur-proyek)
- [Menjalankan Pipeline](#menjalankan-pipeline)
  - [Tahap 1 – Membangun Case Base](#tahap-1--membangun-case-base)
  - [Tahap 2 – Case Representation](#tahap-2--case-representation)
  - [Tahap 3 – Case Retrieval](#tahap-3--case-retrieval)
  - [Tahap 4 – Solution Reuse](#tahap-4--solution-reuse)
  - [Tahap 5 – Model Evaluation](#tahap-5--model-evaluation)
- [Hasil Evaluasi](#hasil-evaluasi)
- [Lisensi & Kredit](#lisensi--kredit)

---

## Overview

Proyek ini mengimplementasikan sistem *Case-Based Reasoning* untuk mendukung analisis dan rekomendasi hukum berdasarkan kasus-kasus sebelumnya. Pipeline ini mencakup lima tahap utama, dimulai dari scraping putusan, ekstraksi informasi, representasi vektor, pengambilan kasus, hingga evaluasi performa model.

---

## Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/Descanden/CBR_putusan-MA.git
cd CBR_putusan-MA

