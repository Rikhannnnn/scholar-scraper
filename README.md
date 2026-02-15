# 🔍 Google Scholar Scraper & Article Similarity Analysis

Sebuah *tool* berbasis web untuk melakukan *scraping* artikel ilmiah dari Google Scholar dan menganalisis tingkat relevansinya terhadap kata kunci pengguna menggunakan pendekatan *Natural Language Processing* (NLP).

Proyek ini menggabungkan **PHP** sebagai antarmuka *frontend* dan **Python** sebagai mesin pemroses data utama (*scraping* & algoritma).

## 🚀 Gambaran Umum

Proyek ini mengotomatisasi proses pencarian referensi jurnal berdasarkan penulis tertentu. Alih-alih mencari secara manual, sistem ini memungkinkan pengguna untuk:
1.  **Scraping Otomatis:** Mengambil data artikel dari profil Google Scholar penulis yang dituju.
2.  **Preprocessing Teks:** Melakukan penerjemahan, *stemming*, dan penghapusan *stopword* untuk standarisasi teks.
3.  **Analisis Kemiripan:** Menghitung seberapa relevan judul artikel dengan kata kunci yang dicari menggunakan metode **TF-IDF** dan **Jaccard Similarity**.
4.  **Ranking:** Menampilkan hasil artikel yang paling relevan beserta metadata lengkapnya (Judul, Penulis, Tanggal, Jurnal, Sitasi).

## 🛠️ Teknologi yang Digunakan

* **Bahasa Pemrograman:**
    * Python (Logic, Scraping, & Data Science)
    * PHP (Server-side scripting & Interface)
* **Library Python Utama:**
    * `Selenium`: Untuk automasi *browser* dan *scraping* data dinamis.
    * `Scikit-learn`: Untuk perhitungan **TF-IDF Vectorizer** dan **Jaccard Score**.
    * `Sastrawi`: Library NLP khusus Bahasa Indonesia untuk proses *Stemming* dan *Stopword Removal*.
    * `Deep-translator`: Untuk menerjemahkan judul artikel dan *keyword* agar berada dalam konteks bahasa yang sama (Indonesia) sebelum dianalisis.

## ✨ Fitur Utama

* **Integrasi PHP & Python:** PHP mengeksekusi skrip Python di latar belakang menggunakan `shell_exec` dan menampilkan hasilnya dalam format JSON.
* **Penerjemahan Otomatis:** Judul artikel berbahasa Inggris diterjemahkan secara otomatis ke Bahasa Indonesia untuk akurasi pencarian.
* **Algoritma NLP:**
    * Mengubah kata berimbuhan menjadi kata dasar (*Stemming*).
    * Membuang kata sambung yang tidak penting (*Stopword Removal*).
* **Metrik Similaritas:** Menggunakan **Jaccard Similarity** pada vektor **TF-IDF** untuk menentukan persentase kemiripan antara *keyword* user dengan judul artikel.

## ⚙️ Instalasi & Cara Menjalankan

### Prasyarat
* Python 3.x
* PHP
* Google Chrome Browser
