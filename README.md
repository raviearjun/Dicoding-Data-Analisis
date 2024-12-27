# Analisis Data Publik E-Commerce dengan Python - Dicoding
![Dasbor Data E-Commerce](dashboard.gif)

[Aplikasi Streamlit Dasbor Data E-Commerce](https://raviearjun.streamlit.app/)

## Daftar Isi
- [Deskripsi Singkat](#deskripsi-singkat)
- [Struktur Proyek](#struktur-proyek)
- [Langkah Instalasi](#langkah-instalasi)
- [Cara Penggunaan](#cara-penggunaan)
- [Sumber Data](#sumber-data)

## Deskripsi Singkat
Proyek ini bertujuan untuk menganalisis dan memvisualisasikan data publik e-commerce menggunakan Python. Proyek mencakup proses persiapan data, eksplorasi data (EDA), serta pembuatan dasbor interaktif menggunakan Streamlit. Fokus analisis adalah memahami pola dari dataset publik e-commerce yang digunakan.

## Struktur Proyek
- `dashboard.py` : kode python untuk streamlit app.
- `data/`: Folder tempat menyimpan file data mentah dalam format CSV.
- `notebook.ipynb`: Notebook Python untuk melakukan analisis data.
- `notebook_ID.ipynb`: Versi notebook.ipynb dalam Bahasa Indonesia.
- `README.md`: File dokumentasi ini.

## Langkah Instalasi
1. Salin repositori ini ke perangkat lokal Anda:
```
git clone https://github.com/raviearjun/Dicoding-Data-Analisis.git
```
2. Masuk ke direktori proyek:
```
cd Dicoding-Data-Analisis
```
3. Pasang pustaka Python yang dibutuhkan:
```
pip install -r requirements.txt
```

## Cara Penggunaan
1. **Persiapan Data**: Gunakan skrip dalam file `notebook.ipynb` untuk membersihkan dan mempersiapkan data.

2. **Eksplorasi Data (EDA)**: Lakukan analisis mendalam pada dataset untuk menemukan pola dan insight dengan bantuan skrip Python yang disediakan.

3. **Visualisasi**: Jalankan dasbor interaktif menggunakan Streamlit dengan perintah berikut:
```
cd Dicoding-Data-Analisis
streamlit run dashboard.py
```
Akses dasbor melalui browser di `http://localhost:8501`.

## Sumber Data
Dataset yang digunakan berasal dari [Proyek Akhir Belajar Analisis Data dengan Python](https://drive.google.com/file/d/1MsAjPM7oKtVfJL_wRp1qmCajtSG1mdcK/view) yang disediakan oleh [Dicoding](https://www.dicoding.com/).

