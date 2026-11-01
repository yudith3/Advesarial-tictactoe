# Adversarial Search: Tic-Tac-Toe 3×3

Aplikasi web untuk bermain Tic-Tac-Toe melawan AI sekaligus **membandingkan lima algoritma adversarial search** pada papan yang sama: Minimax, Alpha-Beta Pruning, Expectimax, Depth-Limited Search (DLS), dan Monte Carlo Tree Search (MCTS).

Seluruh algoritma ditulis dengan Python murni (tanpa library tambahan). Antarmuka web hanya satu file HTML yang memanggil algoritma tersebut lewat API.

---

## Daftar Isi

1. [Fitur](#fitur)
2. [Struktur Proyek](#struktur-proyek)
3. [Cara Menjalankan di Komputer Lokal](#cara-menjalankan-di-komputer-lokal)
4. [Cara Memakai Web](#cara-memakai-web)
5. [Cara Kerja Sistem](#cara-kerja-sistem)
6. [Penjelasan Kelima Algoritma](#penjelasan-kelima-algoritma)
7. [Cara Membaca Hasil Analisis](#cara-membaca-hasil-analisis)
8. [Dokumentasi API](#dokumentasi-api)
9. [Menambah Algoritma Baru](#menambah-algoritma-baru)
10. [Batasan dan Catatan](#batasan-dan-catatan)
11. [Referensi](#referensi)

---

## Fitur

- **Main melawan AI.** Anda bermain sebagai `X`, AI sebagai `O`. Anda bisa memilih siapa yang jalan pertama.
- **Lima algoritma AI** yang bisa diganti kapan saja, bahkan di tengah permainan.
- **Nilai per kotak.** Setelah AI melangkah, skor yang dihitung untuk setiap kotak kosong tampil sebagai angka kecil di kotaknya. Kotak pilihan AI diberi latar kuning.
- **Analisis langkah AI.** Menampilkan langkah terpilih, jumlah node yang dieksplorasi, dan waktu komputasi.
- **Input matriks papan 2D.** Anda bisa menempel posisi papan sendiri dalam bentuk matriks, dan isi kotaknya ikut berubah saat permainan berjalan.
- **Bandingkan semua algoritma.** Satu tombol menjalankan kelima algoritma pada papan saat ini dan menampilkan tabel perbandingan.
- **Parameter yang bisa diatur:** batas kedalaman (DLS) dan jumlah simulasi (MCTS).

---

## Struktur Proyek

```
.
├── public/
│   └── index.html          # Antarmuka web (HTML + CSS + JavaScript dalam satu file)
├── api/
│   ├── move.py             # Endpoint POST /api/move   (khusus Vercel)
│   └── compare.py          # Endpoint POST /api/compare (khusus Vercel)
├── algorithms/
│   ├── __init__.py
│   ├── common.py           # Fungsi bersama: cek pemenang, langkah legal, penilaian, root_search
│   ├── minimax.py          # 1. Minimax
│   ├── alphabeta.py        # 2. Alpha-Beta Pruning
│   ├── expectimax.py       # 3. Expectimax
│   ├── dls.py              # 4. Depth-Limited Search
│   └── mcts.py             # 5. Monte Carlo Tree Search
├── core.py                 # Daftar algoritma + validasi input (dipakai api/*.py)
├── local_server.py         # Server untuk menjalankan di komputer sendiri
└── README.md
```

---

## Cara Menjalankan di Komputer Lokal

**Kebutuhan:** Python 3.8 atau lebih baru. Tidak ada library yang perlu dipasang.

```bash
# 1. masuk ke folder proyek
cd nama-folder-proyek

# 2. jalankan server
python local_server.py

# (opsional) memakai port lain
python local_server.py 5000
```

Lalu buka `http://localhost:8000` di browser (atau port yang Anda pilih).

Untuk menghentikan server, tekan `Ctrl + C` di terminal.

**Jika halaman tidak berubah setelah Anda mengedit `index.html`,** muat ulang dengan `Ctrl + F5` agar cache browser dibersihkan.

---

## Cara Memakai Web

### 1. Bermain melawan AI

1. Pilih **Yang jalan pertama**: Anda (X) atau AI (O), lalu klik **Permainan baru**.
2. Pilih algoritma pada kartu **Algoritma AI**.
3. Klik kotak kosong untuk melangkah. AI akan membalas otomatis.
4. Permainan berakhir saat ada pemenang (tiga tanda sejajar disorot kuning) atau papan penuh (seri).

### 2. Memakai input matriks papan

Kotak **Matriks papan (input 2D)** menampilkan papan saat ini, satu baris matriks per baris papan. Contoh:

```
["X","",""],
["","O",""],
["","",""]
```

- `"X"` dan `"O"` adalah tanda pemain, `""` adalah kotak kosong.
- Matriks harus berukuran 3×3.
- Untuk menguji posisi sendiri: ubah isi kotak, lalu klik **Muat matriks**.
- Format yang salah akan menampilkan pesan error berwarna merah, dan papan tidak berubah.
- Matriks lengkap dengan kurung terluar, misalnya `[["X","",""],["","O",""],["","",""]]`, juga diterima.

**Penentuan giliran saat matriks dimuat:** jika jumlah `X` lebih banyak maka giliran `O`, jika jumlah `O` lebih banyak maka giliran `X`, dan jika sama maka giliran mengikuti pilihan "Yang jalan pertama". Bila giliran jatuh pada AI, AI langsung melangkah.

### 3. Bandingkan semua algoritma

Klik **Jalankan perbandingan** untuk menjalankan kelima algoritma pada papan saat ini, untuk pemain yang sedang mendapat giliran. Papan permainan tidak berubah. Tombol ini tidak bekerja jika permainan sudah selesai.

Tabel hasil berisi langkah yang dipilih tiap algoritma, jumlah node (garis di bawah angka memakai skala logaritmik), dan waktu dalam milidetik.

Saran pengujian untuk laporan:

| Kondisi papan | Yang bisa diamati |
|---|---|
| Papan kosong | Selisih jumlah node terbesar antara Minimax dan Alpha-Beta |
| Papan setengah terisi | Perbedaan langkah antar algoritma mulai terlihat |
| Papan hampir penuh | Semua algoritma cepat dan hasilnya biasanya sama |

Coba juga variasi batas kedalaman DLS (misalnya 1, 3, 5, 9) dan jumlah simulasi MCTS (misalnya 100, 1000, 10000).

---

## Cara Kerja Sistem

```
Browser (public/index.html)
   │  1. Pemain klik kotak → papan diperbarui di JavaScript
   │  2. fetch POST /api/move  { algorithm, board, player, limit, sims }
   ▼
Server Python (local_server.py atau api/move.py)
   │  3. Validasi input
   │  4. Memanggil algorithms/<nama>.get_move(board, me, ...)
   ▼
Algoritma
   │  5. Mencoba setiap langkah legal AI di akar pohon, lalu menilainya
   ▼
Respons JSON { move, scores, nodes, time_ms }
   ▼
Browser: menggambar langkah AI, angka skor di kotak, dan panel analisis
```

Poin penting:

- **Aturan permainan hanya di browser untuk tampilan.** JavaScript mengecek pemenang untuk menampilkan status. Pencarian AI sepenuhnya dilakukan oleh Python.
- **Server tidak menyimpan state.** Setiap permintaan membawa papan lengkap, sehingga server bebas dijalankan ulang atau di-deploy secara serverless.
- **Satu antarmuka untuk semua algoritma.** Kelima file algoritma memiliki fungsi yang sama, yaitu `get_move(board, me, **opsi)`, sehingga mudah dibandingkan dan ditambah.

### Representasi papan

Papan adalah matriks 2D (list of list) berukuran 3×3 berisi `"X"`, `"O"`, atau `""`.

### Kerangka pencarian bersama (`algorithms/common.py`)

Fungsi `root_search` dipakai oleh Minimax, Alpha-Beta, Expectimax, dan DLS:

1. Untuk setiap langkah legal pemain AI di akar, tempatkan tanda di papan.
2. Panggil fungsi `value` milik algoritma untuk menilai papan hasilnya.
3. Simpan skor tiap langkah (inilah angka yang tampil di kotak), lalu batalkan langkah.
4. Pilih langkah dengan skor tertinggi. Jika seri, dipilih yang paling awal (urut dari baris atas, kiri ke kanan).

Dengan cara ini setiap langkah di akar dievaluasi penuh, sehingga skor semua kotak dapat ditampilkan dan hasilnya adil untuk perbandingan.

### Fungsi penilaian

- Kemenangan pemain AI bernilai `100 - kedalaman`, kekalahan bernilai `kedalaman - 100`, seri bernilai `0`.
- Pengurangan kedalaman membuat AI memilih kemenangan tercepat dan menunda kekalahan selama mungkin.

### Penghitungan node

Setiap kali fungsi `value` dipanggil untuk satu keadaan papan, penghitung node bertambah satu. Untuk MCTS, penghitung adalah jumlah node yang dibuat di pohon pencarian (lihat bagian MCTS).

---

## Penjelasan Kelima Algoritma

### 1. Minimax (`algorithms/minimax.py`)

Menelusuri seluruh pohon permainan sampai papan selesai. Pada giliran AI dipilih nilai **maksimum** (MAX), pada giliran lawan dipilih nilai **minimum** (MIN), dengan asumsi lawan bermain sempurna.

- Hasil: selalu optimal.
- Kompleksitas waktu: O(b^d), dengan b faktor percabangan dan d kedalaman. Pada papan kosong ada sekitar 550 ribu node.

### 2. Alpha-Beta Pruning (`algorithms/alphabeta.py`)

Minimax yang membawa dua batas, `alpha` (nilai terbaik yang sudah dijamin untuk MAX) dan `beta` (nilai terbaik yang sudah dijamin untuk MIN). Jika `alpha >= beta`, sisa cabang di bawah node itu tidak mungkin memengaruhi keputusan, sehingga dipangkas.

- Hasil: **identik dengan Minimax** (langkah dan skor sama).
- Kompleksitas: pada kondisi terbaik O(b^(d/2)). Jumlah node jauh lebih sedikit dari Minimax, dan seberapa banyak bergantung pada urutan langkah yang ditelusuri.
- Di proyek ini setiap langkah di akar dicari dengan jendela penuh, sehingga skor tiap kotak persis sama dengan Minimax.

### 3. Expectimax (`algorithms/expectimax.py`)

Node lawan diganti dengan **chance node**: lawan dianggap memilih langkah secara **acak dengan peluang seragam**, sehingga nilainya adalah rata-rata nilai semua langkah lawan. Node AI tetap MAX.

- Cocok jika lawan tidak selalu optimal.
- Jumlah node sama dengan Minimax karena tidak ada pemangkasan, tetapi langkah yang dipilih bisa berbeda, karena AI mengejar nilai harapan, bukan nilai terburuk.
- Skor sering berupa desimal.

### 4. Depth-Limited Search (`algorithms/dls.py`)

Minimax dengan **batas kedalaman**. Saat batas tercapai dan papan belum selesai, papan dinilai dengan **fungsi heuristik**, bukan ditelusuri lebih dalam.

Heuristik yang dipakai, dijumlahkan untuk 8 baris kemenangan (3 baris, 3 kolom, 2 diagonal):

- Baris tanpa tanda lawan: nilai positif sesuai jumlah tanda AI (1 tanda = +1, 2 tanda = +5).
- Baris tanpa tanda AI: nilai negatif sesuai jumlah tanda lawan (1 tanda = −1, 2 tanda = −5).
- Baris yang berisi tanda kedua pemain tidak bernilai (sudah mati).

Batas kedalaman bisa diatur di web (default 3, rentang 1 sampai 9). Batas kecil membuat pencarian cepat tetapi langkahnya bisa kurang tepat. Batas 9 setara dengan Minimax penuh.

### 5. Monte Carlo Tree Search (`algorithms/mcts.py`)

Tidak menelusuri semua kemungkinan, melainkan membangun pohon secara bertahap lewat simulasi. Setiap iterasi melalui empat tahap:

1. **Selection**: turun dari akar dengan memilih anak berdasarkan rumus UCB1 (`rata-rata hasil + 1.41 × √(ln N / n)`), yang menyeimbangkan eksploitasi dan eksplorasi.
2. **Expansion**: tambahkan satu anak baru dari langkah yang belum dicoba.
3. **Simulation**: mainkan acak sampai permainan selesai.
4. **Backpropagation**: perbarui hasil (menang 1, seri 0,5, kalah 0) di sepanjang jalur kembali ke akar.

Langkah akhir adalah anak akar yang paling sering dikunjungi. Jumlah simulasi bisa diatur di web (default 1000).

Karena memakai pengacakan, **hasil MCTS dapat berbeda setiap kali dijalankan**. Kolom "node" untuk MCTS berarti jumlah node pohon yang dibuat, yang definisinya berbeda dari algoritma lain, jadi perbandingan langsungnya perlu diberi catatan.

### Ringkasan perbandingan

| Algoritma | Asumsi lawan | Optimal? | Deterministik? | Pemangkasan |
|---|---|---|---|---|
| Minimax | Optimal | Ya | Ya | Tidak |
| Alpha-Beta | Optimal | Ya | Ya | Ya |
| Expectimax | Acak | Tidak selalu | Ya | Tidak |
| DLS | Optimal (terbatas kedalaman) | Tergantung batas | Ya | Tidak |
| MCTS | Acak (lewat simulasi) | Mendekati, tergantung simulasi | Tidak | Tidak |

---

## Cara Membaca Hasil Analisis

### Panel analisis langkah AI

| Item | Arti |
|---|---|
| Langkah terpilih | Posisi pilihan AI sebagai (baris, kolom), mulai dari 1 |
| Node dieksplorasi | Jumlah keadaan papan yang dikunjungi saat mencari langkah. Ukuran biaya yang tidak bergantung pada kecepatan komputer |
| Waktu | Lama pencarian dalam milidetik. Dipengaruhi kondisi komputer |

### Angka kecil di kotak

Skor langkah di kotak itu dari sudut pandang AI. Kotak dengan skor tertinggi dipilih AI.

| Algoritma | Arti angka |
|---|---|
| Minimax, Alpha-Beta | Positif: AI bisa menang (makin besar makin cepat menang). Negatif: AI kalah. Nol: seri |
| Expectimax | Skala sama, tetapi berupa rata-rata sehingga sering desimal |
| DLS | Jika hasil akhir terlihat dalam batas kedalaman, nilainya seperti Minimax. Jika tidak, berupa angka heuristik kecil |
| MCTS | Rasio hasil simulasi dari 0 sampai 1 (menang 1, seri 0,5, kalah 0) |

Skor hilang saat Anda melangkah lagi.

---

## Dokumentasi API

Semua endpoint memakai metode `POST` dengan isi JSON.

### `POST /api/move`

Menjalankan satu algoritma.

**Request**
```json
{
  "algorithm": "minimax",
  "board": [["X", "", ""], ["", "O", ""], ["", "", ""]],
  "player": "O",
  "limit": 3,
  "sims": 1000
}
```

| Field | Keterangan |
|---|---|
| `algorithm` | `minimax`, `alphabeta`, `expectimax`, `dls`, atau `mcts` |
| `board` | Matriks 3×3 berisi `"X"`, `"O"`, atau `""` |
| `player` | Pemain yang akan melangkah, `"X"` atau `"O"` (default `"O"`) |
| `limit` | Batas kedalaman, hanya dipakai DLS (default 3) |
| `sims` | Jumlah simulasi, hanya dipakai MCTS (default 1000) |

**Response (200)**
```json
{
  "move": [0, 1],
  "scores": {"0,1": 0, "0,2": 0, "1,0": 0},
  "nodes": 3025,
  "time_ms": 4.812
}
```

| Field | Keterangan |
|---|---|
| `move` | Langkah terpilih `[baris, kolom]` mulai dari 0, atau `null` jika permainan sudah selesai |
| `scores` | Skor tiap langkah legal, dengan kunci `"baris,kolom"` mulai dari 0 |
| `nodes` | Jumlah node yang dieksplorasi |
| `time_ms` | Waktu pencarian dalam milidetik |

### `POST /api/compare`

Menjalankan kelima algoritma. Request sama seperti di atas (field `algorithm` diabaikan). Response berupa objek dengan kunci nama algoritma, masing-masing berisi `move`, `scores`, `nodes`, dan `time_ms`.

### Error

Input yang tidak valid mengembalikan status `400`:
```json
{"error": "Papan harus matriks 3x3 berisi 'X', 'O', atau ''."}
```

Contoh memanggil dengan `curl`:
```bash
curl -X POST http://localhost:8000/api/move \
  -H "Content-Type: application/json" \
  -d '{"algorithm":"alphabeta","board":[["X","",""],["","",""],["","",""]],"player":"O"}'
```

---

## Menambah Algoritma Baru

1. Buat file `algorithms/nama_algoritma.py` dengan fungsi:
   ```python
   def get_move(board, me, **_):
       ...
       return {"move": [r, c], "scores": {"r,c": nilai}, "nodes": jumlah, "time_ms": ms}
   ```
   Jika algoritmanya berbasis nilai papan, cukup tulis fungsi `value(b, turn, d, ctx, me)` dan panggil `root_search(board, me, value)` dari `common.py`.
2. Daftarkan di `ALGOS` pada `core.py` (dan di `local_server.py` jika dipakai).
3. Tambahkan nama dan deskripsinya pada objek `NAMES` dan `DESC` di `public/index.html`.

---

## Batasan dan Catatan

- Ukuran papan tetap 3×3. Algoritma memakai pencarian penuh, sehingga papan yang lebih besar akan jauh lebih lambat.
- Pemain manusia selalu `X` dan AI selalu `O` pada mode bermain. Fitur perbandingan memakai pemain mana pun yang sedang mendapat giliran.
- Waktu komputasi bergantung pada perangkat. Jumlah node adalah ukuran yang lebih stabil untuk membandingkan algoritma.
- MCTS memakai pengacakan sehingga hasilnya bisa berbeda antar eksekusi.
- Seri pada skor tertinggi dipecahkan dengan memilih langkah paling awal (kecuali MCTS, yang memilih berdasarkan jumlah kunjungan).

---

## Referensi

- GeeksforGeeks, *Adversarial Search Algorithms in Artificial Intelligence*: https://www.geeksforgeeks.org/artificial-intelligence/adversarial-search-algorithms/
- Russell, S. & Norvig, P., *Artificial Intelligence: A Modern Approach* (bab Adversarial Search and Games).