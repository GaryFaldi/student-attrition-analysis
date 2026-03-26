# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding

Jaya Jaya Institut merupakan institusi pendidikan perguruan tinggi yang telah berdiri sejak tahun 2000. Hingga saat ini, institusi ini telah mencetak banyak lulusan dengan reputasi yang sangat baik. Namun, seiring berjalannya waktu, pihak manajemen mulai menyadari adanya fenomena yang mengkhawatirkan, yaitu tingginya jumlah mahasiswa yang tidak menyelesaikan pendidikannya (dropout).

Masalah dropout ini tidak hanya merugikan mahasiswa secara personal, tetapi juga berdampak negatif terhadap reputasi institusi, menurunkan efisiensi operasional, serta menghambat pencapaian kualitas output pendidikan yang diharapkan. Selama ini, pihak institusi belum memiliki sistem yang mampu memetakan faktor-faktor penyebab dropout secara mendalam maupun mendeteksi mahasiswa yang berisiko tinggi sejak dini.

### Permasalahan Bisnis

1. **Tingginya angka dropout** — Institusi menghadapi tantangan serius terkait banyaknya mahasiswa yang tidak menyelesaikan masa studinya. Fenomena ini jika dibiarkan akan merusak reputasi akademik Jaya Jaya Institut dan menurunkan efisiensi operasional pendidikan.
2. **Tidak adanya sistem deteksi dini** — Saat ini, institusi belum memiliki sistem atau alat bantu yang mampu mengidentifikasi mahasiswa dengan risiko dropout tinggi secara proaktif. Hal ini menyebabkan penanganan terhadap mahasiswa yang bermasalah seringkali terlambat (setelah mahasiswa tersebut benar-benar keluar).
3. **Belum dipahaminya faktor penyebab dropout** — Belum adanya analisis komprehensif mengenai faktor apa saja (baik dari sisi akademik, kondisi finansial, maupun latar belakang demografis) yang paling kuat berkontribusi terhadap keputusan mahasiswa untuk berhenti studi.terhadap dropout.

### Cakupan Proyek

- Eksplorasi dan analisis data performa mahasiswa (EDA)
- Identifikasi faktor-faktor yang berkorelasi dengan dropout
- Pembangunan model machine learning untuk prediksi status mahasiswa (Dropout / Enrolled / Graduate)
- Pembuatan business dashboard dengan metabase
- Pengembangan prototype aplikasi prediksi berbasis Streamlit

### Persiapan

**Sumber data:** [Students' Performance Dataset — UCI Machine Learning Repository](https://doi.org/10.24432/C5MC89)  
Dataset berisi 4.424 baris dan 37 kolom mencakup informasi akademik, demografis, dan sosial-ekonomi mahasiswa.

#### 1. Clone Repository

Silahkan Download semua file yang ada di Gdrive: [https://drive.google.com/drive/folders/1EfR-EucVlEGSZSZSkZcHQJj5eOEkgBgl?usp=sharing](https://drive.google.com/drive/folders/1EfR-EucVlEGSZSZSkZcHQJj5eOEkgBgl?usp=sharing)

#### 2. Membuat Virtual Environment

```bash
python -m venv venv
```

#### 3. Mengaktifkan Virtual Environment

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

#### 4. Menginstal Dependensi

```bash
pip install -r requirements.txt
```

---

## Business Dashboard

Dashboard dibuat menggunakan **Metabase** dan menampilkan visualisasi data mahasiswa Jaya Jaya Institut secara komprehensif. Dashboard terdiri dari dua halaman:

**Halaman 1 — Overview & Demografi:**
- **Distribusi Status Mahasiswa** — Donut chart menunjukkan 49.9% Graduate, 32.1% Dropout, 17.9% Enrolled dari total 4.424 mahasiswa
- **Perbandingan Umur saat Mendaftar per Status** — Kelompok usia 15–22.5 tahun mendominasi, terutama pada kelompok Graduate
- **Rasio Gender per Status** — Mahasiswa laki-laki memiliki proporsi dropout lebih tinggi dibanding perempuan
- **Rata-rata Nilai Saat Mendaftar vs Status** — Perbedaan admission grade antar status relatif tipis (~125), menunjukkan nilai masuk bukan satu-satunya penentu kelulusan

**Halaman 2 — Faktor Finansial & Akademik:**
- **Status Beasiswa terhadap Status Mahasiswa** — Penerima beasiswa memiliki dropout rate ~12%, jauh lebih rendah dari non-penerima (~38%)
- **Status Hutang terhadap Status Mahasiswa** — Mahasiswa yang memiliki hutang berisiko dropout 2x lebih tinggi (~62%)
- **Rata-rata Nilai Semester 1 & 2 per Status** — Dropout memiliki rata-rata nilai sangat rendah (~6–7), sedangkan Graduate konsisten di ~12.5
- **Rata-rata Mata Kuliah Lulus per Status** — Dropout rata-rata hanya lulus ~2 MK per semester, Graduate lulus ~6 MK

**Akses Dashboard Metabase:**
- Email: `root@mail.com`
- Password: `root123`

---

## Menjalankan Sistem Machine Learning

Prototype sistem prediksi dropout dibuat menggunakan **Streamlit** dengan fitur:
- **Prediksi Manual** — Input data satu mahasiswa, hasil prediksi Dropout/Enrolled/Graduate beserta gauge probabilitas
- **Prediksi Batch** — Upload CSV untuk prediksi banyak mahasiswa sekaligus, lengkap dengan ringkasan dan download hasil
- **Pilihan Model** — Tersedia 4 model: Random Forest, XGBoost, Logistic Regression, SVM

**Menjalankan secara lokal:**

```bash
streamlit run app.py
```

Pastikan folder `models/` berisi file hasil training:

```
models/
├── random_forest.pkl
├── xgboost.pkl
├── logistic_regression.pkl
├── svm.pkl
├── scaler.pkl
└── feature_names.pkl
```

**Link prototype:** [https://student-attrition-analysis.streamlit.app](https://student-attrition-analysis.streamlit.app)

---

## Conclusion

Berdasarkan hasil analisis data dan pemodelan machine learning, diperoleh kesimpulan sebagai berikut:

**Beberapa faktor penyebab dropout:**

1. **Performa akademik semester awal** adalah prediktor terkuat. Mahasiswa dropout rata-rata memiliki nilai semester 0–7 dan hampir tidak ada mata kuliah yang lulus (0–2 MK), dibandingkan Graduate yang konsisten di nilai ~12.5 dan lulus ~6 MK per semester.

2. **Faktor finansial sangat menentukan:**
   - Mahasiswa yang **menunggak uang kuliah** memiliki dropout rate ~85%
   - Mahasiswa yang **memiliki hutang** berisiko dropout 2x lebih tinggi (~62%)
   - Penerima **beasiswa** memiliki dropout rate hanya ~12%

3. **Latar belakang keluarga** berpengaruh — Kualifikasi pendidikan orang tua yang rendah berkorelasi dengan tingkat dropout yang lebih tinggi pada kategori-kategori tertentu (hingga 100% dropout rate).

4. **Usia pendaftaran** — Mahasiswa yang masuk di usia lebih tua (>30 tahun) cenderung memiliki risiko dropout lebih tinggi dibanding mahasiswa usia 15–22 tahun.

####  Evaluasi Performa Model

Bagian ini merinci hasil eksperimen beberapa algoritma *machine learning* untuk menentukan model terbaik dalam memprediksi status akademik mahasiswa (*Dropout, Enrolled, Graduate*).

#### 1. Perbandingan Performa Antar Model
Berdasarkan pengujian menggunakan metrik standar klasifikasi, berikut adalah ringkasan performa dari seluruh model yang diuji:

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest** | **0.8960** | **0.8926** | **0.8960** | **0.8902** | **0.9679** |
| XGBoost | 0.8904 | 0.8886 | 0.8904 | 0.8894 | 0.9660 |
| Logistic Regression | 0.8576 | 0.8806 | 0.8576 | 0.8637 | 0.9646 |
| SVM | 0.8565 | 0.8801 | 0.8565 | 0.8629 | 0.9656 |

> **Kesimpulan:** **Random Forest** dipilih sebagai model terbaik karena unggul di seluruh metrik utama, terutama pada nilai **ROC-AUC (0.9679)** dan **Accuracy (89.6%)**.

---

#### 2. Detail Klasifikasi: Random Forest (Best Model)
Untuk memahami performa model pada setiap label kategori, berikut adalah detail *Classification Report* dari model Random Forest:

| Class | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| **Dropout** | 1.00 | 1.00 | 1.00 | 284 |
| **Enrolled** | 0.79 | 0.57 | 0.66 | 159 |
| **Graduate** | 0.86 | 0.95 | 0.90 | 442 |
| | | | | |
| **Accuracy** | | | **0.90** | **885** |
| **Macro Avg** | 0.88 | 0.84 | 0.86 | 885 |
| **Weighted Avg** | 0.89 | 0.90 | 0.89 | 885 |

#### **Analisis Hasil:**
* **Prediksi Dropout Sempurna:** Model memiliki performa sempurna (Score: 1.00) dalam mendeteksi kelas *Dropout*. Hal ini sangat penting untuk memberikan intervensi tepat sasaran.
* **Akurasi Lulusan Tinggi:** Model sangat kuat dalam mengenali mahasiswa yang akan lulus (*Graduate*) dengan F1-Score sebesar **0.90**.
* **Tantangan Kelas Enrolled:** Kelas *Enrolled* memiliki skor terendah (F1: 0.66). Ini menunjukkan adanya kemiripan pola data antara mahasiswa yang masih aktif dengan mereka yang berpotensi lulus atau dropout di masa mendatang.

---

#### 3. Ringkasan Akhir
Model **Random Forest** memberikan keseimbangan terbaik antara presisi dan daya panggil (*recall*). Dengan nilai **ROC-AUC mendekati 1.0**, model ini terbukti sangat reliabel untuk digunakan dalam sistem prediksi status keberlanjutan studi mahasiswa.

### Rekomendasi Action Items

- **Implementasi sistem early warning berbasis model** — Gunakan prototype Streamlit untuk mendeteksi mahasiswa berisiko dropout sejak akhir semester pertama, sebelum kondisi semakin parah.
- **Program intervensi finansial** — Perluas program beasiswa dan skema cicilan UKT bagi mahasiswa yang menunggak atau memiliki hutang, mengingat faktor finansial adalah prediktor dropout terkuat kedua setelah performa akademik.
- **Bimbingan akademik intensif di semester awal** — Identifikasi mahasiswa dengan nilai rendah atau 0 MK lulus di semester 1 dan segera berikan program tutoring/mentoring karena pola ini sangat prediktif terhadap dropout.
- **Program khusus untuk mahasiswa non-tradisional** — Sediakan dukungan tambahan bagi mahasiswa yang mendaftar di usia >30 tahun atau yang berasal dari latar belakang pendidikan keluarga rendah.
- **Monitoring dashboard berkala** — Gunakan business dashboard Metabase secara rutin (minimal per semester) untuk memantau tren dropout per program studi, kelompok usia, dan status finansial mahasiswa.
