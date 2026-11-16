# Proyek Analisis Data: Air Quality Dataset (Beijing, 2013–2017)

Proyek akhir kelas Dicoding **"Belajar Analisis Data dengan Python"**,
menggunakan **Air Quality Dataset** (PRSA Beijing Multi-Site Air-Quality
Data, 12 stasiun pemantauan, periode Maret 2013–Februari 2017).

## Struktur Direktori

```
submission
├───dashboard
│   ├───main_data.csv      # data bersih hasil tahap Data Wrangling
│   └───dashboard.py       # aplikasi dashboard Streamlit
├───data
│   └───PRSA_Data_*.csv    # 12 dataset mentah per stasiun
├───notebook.ipynb         # notebook proses analisis data lengkap
├───README.md
├───requirements.txt
└───url.txt
```

## Setup Environment

Disarankan menggunakan virtual environment agar dependensi tidak bentrok
dengan sistem.

```shell
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Menjalankan Notebook Analisis

Notebook `notebook.ipynb` berisi seluruh proses analisis data mulai dari
penentuan pertanyaan bisnis, data wrangling (gathering, assessing,
cleaning), exploratory data analysis, visualisasi & explanatory analysis,
analisis lanjutan (geospatial & clustering manual/binning), hingga
conclusion & recommendation.

```shell
jupyter notebook notebook.ipynb
```

atau buka langsung dengan Jupyter Lab / Google Colab (upload notebook dan
folder `data/`).

> Notebook membaca dataset mentah dari folder `data/` secara relatif
> (`data/PRSA_Data_*.csv`), jadi jalankan notebook dari direktori
> `submission/` (root proyek).

## Menjalankan Dashboard secara Lokal

Dashboard Streamlit (`dashboard/dashboard.py`) menampilkan ringkasan hasil
analisis secara interaktif: filter rentang tanggal, stasiun, dan jenis
polutan; tren waktu; perbandingan antar stasiun; peta sebaran geospasial;
serta distribusi kategori kualitas udara (hasil binning manual).

```shell
cd dashboard
streamlit run dashboard.py
```

Dashboard akan terbuka otomatis di browser pada `http://localhost:8501`.
Dashboard membaca `main_data.csv` yang berada di folder yang sama
(`dashboard/main_data.csv`), jadi pastikan kedua berkas tetap berada dalam
satu folder saat dijalankan maupun saat di-deploy.

## Men-deploy ke Streamlit Community Cloud

Deployment memerlukan akun GitHub dan akun Streamlit Community Cloud milik
masing-masing pengguna, sehingga perlu dilakukan secara mandiri dengan
langkah berikut:

1. Push folder `submission/` ini (atau minimal isi folder `dashboard/`
   beserta `requirements.txt`) ke sebuah repository GitHub.
2. Daftar/masuk ke [Streamlit Community Cloud](https://share.streamlit.io/)
   menggunakan akun GitHub Anda.
3. Klik **"New app"**, pilih repository, branch, dan set **Main file
   path** ke `dashboard/dashboard.py`.
4. Klik **Deploy**. Tunggu proses build selesai.
5. Setelah berhasil, salin URL aplikasi (format
   `https://<nama-app>.streamlit.app`) dan tempelkan ke berkas `url.txt`.

## Insight Utama

Ringkasan temuan selengkapnya beserta visualisasi dan penjelasannya dapat
dilihat pada bagian akhir `notebook.ipynb` (Conclusion). Secara singkat:

- Konsentrasi PM2.5 di Beijing menunjukkan pola musiman yang kuat, dengan
  **musim dingin** sebagai periode risiko tertinggi.
- Terdapat variasi spasial yang jelas antar stasiun — stasiun di area
  padat perkotaan cenderung mencatat PM2.5 lebih tinggi dibanding stasiun
  di wilayah pinggiran.
- Pola harian menunjukkan konsentrasi PM2.5 cenderung meningkat pada malam
  hingga dini hari.

## Sumber Data

Beijing Multi-Site Air-Quality Data (PRSA), 2013–2017 —
<https://github.com/marceloreis/HTI/tree/master>
