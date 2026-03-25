# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding

Jaya Jaya Institut merupakan institusi pendidikan perguruan tinggi yang telah berdiri sejak tahun 2000. Hingga saat ini institusi ini telah mencetak banyak lulusan dengan reputasi yang sangat baik. Namun demikian, terdapat permasalahan serius berupa tingginya angka mahasiswa yang tidak menyelesaikan pendidikannya alias **dropout** (32.1% dari total 4.424 mahasiswa).

Tingginya angka dropout berdampak negatif terhadap reputasi institusi, efisiensi operasional, dan kualitas output pendidikan. Oleh karena itu, Jaya Jaya Institut ingin mendeteksi sedini mungkin mahasiswa yang berpotensi dropout sehingga dapat diberikan bimbingan dan intervensi khusus sebelum terlambat.

### Permasalahan Bisnis

1. **Tingginya angka dropout** — 32.1% mahasiswa (1.421 dari 4.424) tidak menyelesaikan studi, angka yang signifikan bagi reputasi institusi.
2. **Tidak adanya sistem deteksi dini** — Institusi belum memiliki mekanisme untuk mengidentifikasi mahasiswa berisiko dropout secara proaktif.
3. **Belum dipahaminya faktor penyebab dropout** — Perlu analisis mendalam terhadap faktor akademik, finansial, dan demografis yang berkontribusi terhadap dropout.

### Cakupan Proyek

- Eksplorasi dan analisis data performa mahasiswa (EDA)
- Identifikasi faktor-faktor yang berkorelasi dengan dropout
- Pembangunan model machine learning untuk prediksi status mahasiswa (Dropout / Enrolled / Graduate)
- Pembuatan business dashboard untuk monitoring performa mahasiswa
- Pengembangan prototype aplikasi prediksi berbasis Streamlit

### Persiapan

**Sumber data:** [Students' Performance Dataset — UCI Machine Learning Repository](https://doi.org/10.24432/C5MC89)  
Dataset berisi 4.424 baris dan 37 kolom mencakup informasi akademik, demografis, dan sosial-ekonomi mahasiswa.

#### 1. Clone Repository

Silahkan Download semua file yang ada di Gdrive: [https://drive.google.com/drive/folders/1LRtRMhq6sHkRJZvTg32Xb3j7BD8D5ONH?usp=drive_link](https://drive.google.com/drive/folders/1LRtRMhq6sHkRJZvTg32Xb3j7BD8D5ONH?usp=drive_link)

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

**Performa model machine learning:**

| Model | Accuracy | F1-Score | ROC-AUC |
|---|---|---|---|
| **Random Forest** | **0.8960** | **0.8902** | **0.9679** |
| XGBoost | 0.8904 | 0.8894 | 0.9660 |
| Logistic Regression | 0.8576 | 0.8637 | 0.9646 |
| SVM | 0.8565 | 0.8629 | 0.9656 |

**Random Forest** dipilih sebagai model terbaik dengan ROC-AUC **0.9679** dan Accuracy **89.6%**.

### Rekomendasi Action Items

- **Implementasi sistem early warning berbasis model** — Gunakan prototype Streamlit untuk mendeteksi mahasiswa berisiko dropout sejak akhir semester pertama, sebelum kondisi semakin parah.
- **Program intervensi finansial** — Perluas program beasiswa dan skema cicilan UKT bagi mahasiswa yang menunggak atau memiliki hutang, mengingat faktor finansial adalah prediktor dropout terkuat kedua setelah performa akademik.
- **Bimbingan akademik intensif di semester awal** — Identifikasi mahasiswa dengan nilai rendah atau 0 MK lulus di semester 1 dan segera berikan program tutoring/mentoring karena pola ini sangat prediktif terhadap dropout.
- **Program khusus untuk mahasiswa non-tradisional** — Sediakan dukungan tambahan bagi mahasiswa yang mendaftar di usia >30 tahun atau yang berasal dari latar belakang pendidikan keluarga rendah.
- **Monitoring dashboard berkala** — Gunakan business dashboard Metabase secara rutin (minimal per semester) untuk memantau tren dropout per program studi, kelompok usia, dan status finansial mahasiswa.
