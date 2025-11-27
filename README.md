# AES-256 CBC File Encryptor (CLI)

**Tugas Kriptografi Mata Kuliah Keamanan Data**
**Program Studi S1 Data Sains - Telkom University**

Aplikasi ini adalah perangkat lunak berbasis *Command-Line Interface* (CLI) yang berfungsi untuk mengamankan dataset tabular (CSV, TXT) menggunakan algoritma kriptografi **AES-256** dalam mode **CBC** (*Cipher Block Chaining*).

Proyek ini dibuat untuk memenuhi Tugas Individu/Kelompok dengan implementasi algoritma Block Cipher standar NIST.

---

## 👥 Anggota Kelompok

| Nama | NIM |
| :--- | :--- |
| **Safwan Hasbi Asfahani** | 103052300023 |
| **Haekhal M Syaed** | 103052300033 |
| **Kevin Sandy Dimpos Manurung** | 103052300043 |
| **Rizky Nur Widyatmoko** | 103052300053 |

---

## 🚀 Fitur Utama

* **AES-256 CBC:** Menggunakan standar enkripsi industri yang aman (Block Cipher).
* **PBKDF2 Key Derivation:** Mengubah password teks menjadi kunci 256-bit yang aman menggunakan *Salt* acak dan 100.000 iterasi SHA-256.
* **PKCS7 Padding:** Menangani file dengan ukuran berapapun (tidak harus kelipatan 16 byte) secara otomatis.
* **Secure Storage:** Menyimpan hasil enkripsi dalam format Hex yang menggabungkan `Salt + IV + Ciphertext` dalam satu file output.
* **Size Validation:** Mencegah pemrosesan file di atas 1 MB untuk efisiensi memori.

---

## ⚙️ Persiapan & Instalasi

Pastikan Anda sudah menginstal Python 3.13 atau versi terbaru.

1.  **Download** folder proyek ini.
2.  Buka terminal (VS Code atau CMD) dan arahkan ke folder proyek `TUGAS_KRIPTOGRAFI`.
3.  Install library yang dibutuhkan:

```bash
pip install -r requirements.txt
```
--- 

## 📖 Cara Penggunaan

Jalankan perintah berikut melalui terminal dari dalam folder utama proyek.

### 1. Enkripsi File
Mengubah file asli (dataset.csv) menjadi file terenkripsi.

```bash
python source/cli.py encrypt dataset/dataset.csv results/dataset.enc -p rahasia123
```

### 2. Dekripsi File
Fitur ini digunakan untuk mengembalikan file yang sudah terenkripsi (format Hex) menjadi file asli yang bisa dibaca kembali.

**Format Perintah:**
```bash
python source/cli.py decrypt results/dataset.enc results/dataset_decrypt.csv -p rahasia123
```

## 📂 Struktur Proyek

Berikut adalah susunan folder dan file dalam proyek ini beserta penjelasannya:

```text
KRIPTOGRAFI/
│
├── dataset/                  # Folder penyimpanan file Input & Output
│   └── dataset.csv           # File asli (Target Enkripsi)
│
├── source/                   # Folder Kode Program (Source Code)
│   ├── cli.py                # [Frontend] Interface Terminal
│   └── aes_utils.py          # [Backend] Logika AES, Padding, & Key Derivation
│
├── results/                  # Folder Hasil (.enc, .csv)
│
├── requirements.txt          # Daftar library Python
└── README.md                 # Dokumentasi ini
```

## 🔐 Format Data Output

File hasil enkripsi disimpan dalam format **Heksadesimal (Hex String)**. Kami memilih format ini agar hasil enkripsi aman disimpan dalam file teks biasa (.txt) tanpa risiko korupsi data akibat karakter biner yang tidak tercetak.

Secara internal, data disusun dengan urutan penggabungan (*concatenation*) sebagai berikut:

`[Salt (16 Byte)]` + `[IV (16 Byte)]` + `[Ciphertext (Variable)]`

### Rincian Komponen Data:

1.  **Salt (16 Byte / 32 Karakter Hex)**
    * **Fungsi:** Data acak yang digunakan saat proses derivasi kunci (*Key Derivation*) dari password.
    * **Tujuan:** Mencegah serangan *Rainbow Table* dan memastikan bahwa password yang sama akan menghasilkan kunci enkripsi yang berbeda setiap kali program dijalankan.

2.  **IV (Initialization Vector) (16 Byte / 32 Karakter Hex)**
    * **Fungsi:** Vektor inisialisasi acak yang wajib ada untuk algoritma AES mode CBC.
    * **Tujuan:** Mengacak blok pertama data. Ini memastikan bahwa jika kita mengenkripsi dua file yang isinya sama persis (misal: "Halo"), hasil *ciphertext*-nya akan tetap berbeda total.

3.  **Ciphertext (Panjang Bervariasi)**
    * **Fungsi:** Data asli yang telah melalui proses *Padding* (PKCS7) dan dienkripsi dengan kunci AES-256.
    * **Tujuan:** Menyembunyikan informasi asli sehingga tidak bisa dibaca tanpa kunci yang tepat.

### Mekanisme Pembacaan (Dekripsi):
Saat program melakukan dekripsi, string Hex akan dipotong-potong kembali dengan logika:
* **32 karakter pertama** diambil sebagai **Salt**.
* **32 karakter kedua** diambil sebagai **IV**.
* **Sisa karakter** dianggap sebagai **Ciphertext**.
