Nama : Maulana Farrel Arvindra

NPM : 2506552802

Kelas : PBP F

Program Studi: Sistem Informasi

### Tugas 1

1. Saya menggunakan elemen semantik. Penggunaan elemen semantik ini membantu dalam membangun struktur static web yang memiliki makna, bukan hanya membagi ruang visual. Hal ini membuat code lebih rapi dan lebih mudah dibaca. Selain itu, elemen semantik meningkatkan Accesibility dan Search Engine Optimization.
2. Tantangan terbesar biasanya muncul pada elemen yang berjajar secara horizontal di dekstop. Saat layar menyusut ke ukuran mobile, elemen-elemen rentan terpotong, bentuknya memanjang secara tidak proporsional, atau konten teks dan gambar saling bertumpuk. Evaluasi dilakukan dengan melihat logical flow informasi. Pada layar kecil, pergerakan mata pengguna adalah vertikal dari atas ke bawah. Elemen yang berjajar secara horizontal dijajarkan secara vertikal
3. Batasan utama yang saya rasakan dari static web murni ini adalah minimnya interaktivitas untuk mengontrol fokus visual pengguna. Saya ingin menyorot (highlight) satu elemen tertentu (misalnya kartu proyek), namun penyajiannya kurang maksimal karena elemen-elemen lain di halaman tetap tampil penuh dan mendominasi layar.

Berdasarkan batasan tersebut, fungsionalitas dinamis yang paling ingin saya tambahkan pada iterasi selanjutnya adalah pembuatan sistem Modal atau Popup interaktif menggunakan JavaScript. Saya ingin menambahkan event listener sehingga ketika sebuah elemen diklik, informasi detailnya akan muncul dalam bentuk popup, sementara sisa halaman di latar belakang menjadi redup (overlay). Ini akan memberikan pengalaman pengguna (UX) yang jauh lebih fokus dan optimal

AI Disclosure:
Saya menggunakan gemini pro untuk membantu saya membuat elemen dalam list bergerak. Saya menyertakan contoh agar output Ai yang dihasilkan maksimal. Contoh prompt:
"Buatlah implementasi marque mirip seperti contoh yang kuberikan pada list item di section kedua"

### Tugas 2
1. Ketika user melakukan request ke web, request akan diterima oleh urls.py. jika url tersebut cocok dengan endpoint yang ada, url akan memanggil fungsi di dalam views.py. View kemudian berinteraksi dengan model untuk mengambil data dari database. setelah data berhasil diambil, view akan mengirimkan data ke sebuah template. template disini berfungsi sebagai placeholder yang nantinya isinya akan diganti dengan data. hasil gabungan data dengan template akan dikirim sebagai respons untuk dirender dan ditampilkan di browser

2. Jika data disimpan secara manual, setiap kali ada penambahan atau modifikasi pada aplikasi, struktur kode html harus diganti dan hasilnya harus dideploy ulang. Dengan menggunakan model, setiap pembaruan data dapat dilakukan tanpa mengubah file kode dan redeploy. Pendekatan ini memungkinkan aplikasi menangani data yang terus bertambah tanpa mempersulit kode

3. Perintah makemigrations berfungsi untuk mengscan setiap perubahan yang ada di models.py, lalu membuat file skrip migrasi. Perintah migrate akan mengeksekusi skrip migrasi dan membuat table berdasarkan model. Ketika ingin menambah atribut pada suatu model, makemigrations dijalankan untuk membuat skrip migrasi dengan atribut yang ditambahkan. Setelah itu, jika migrate dijalankan, atribut baru tersebut akan ditambahkan menjadi kolom dalam tabel database.

AI Disclosure:
Proyek ini dikembangkan dengan bantuan AI generatif khusus untuk bagian berikut:
+ Pembuatan markup HTML dan styling CSS.
+ Penulisan dan strukturisasi unit test.
Logika inti, arsitektur sistem, dan komponen lainnya dikerjakan secara mandiri.


### Tugas 3
1. Model form Django akan secara otomatis menerjemahkan struktur model menjadi field form HTML yang sesuai. Input juga otomatis divalidasi berdasarkan definisi model. Penggunaan {% csrf_token %} digunakan sebagai mekanisme keamanan bawaan Django untuk mencegah serangan Cross-Site Request Forgery.
2. JSON adalah format turunan asli dari Javascript sehingga sangat kompatibel dengan browser yang dapat memahami javascript.
3. Alur view saat mengembalikan data portofolio JSON:
    1. URL dispatcher Django menerima HTTP Request dari klien dan mengarahkannya ke fungsi/class view yang sesuai.
    2. View berinteraksi dengan model Django menggunakan ORM untuk mengambil data portofolio dari database (menghasilkan objek QuerySet)
    3. QuerySet yang berisi objek model portofolio diubah strukturnya menjadi format tipe data bawaan Python (seperti list atau dictionary).
    4. Data Python tersebut dikonversi (di-dump) menjadi teks berformat JSON.
    5. View membungkus data JSON tersebut ke dalam objek JsonResponse (atau HttpResponse dengan header application/json) dan mengirimkannya kembali ke klien.
    Serialisasi bertugas menerjemahkan objek kompleks menjadi representasi standar seperti JSON.

AI disclosure:
Pada tugas kali ini, saya tidak menggunakan AI sedikitpun. Saya mengikuti apa yang dilakukan di tutorial

### Week 4
AI Disclosure:
“Project ini dikembangkan dengan bantuan AI sebagai asisten dalam penyusunan ide, struktur, dan perbaikan kode berdasarkan prompt yang saya berikan. Semua keputusan akhir, revisi, dan validasi tetap dilakukan oleh saya agar hasilnya sesuai dengan kebutuhan dan kualitas yang diinginkan.”

### Week 5

1. **Debouncing** adalah teknik menunda eksekusi suatu fungsi sampai tidak ada
   input baru selama jangka waktu tertentu. Pada pencarian AJAX, timer diatur
   ulang setiap kali pengguna mengetik. Permintaan pencarian baru dikirim setelah
   pengguna berhenti mengetik, sehingga tidak perlu mengirim request untuk
   setiap karakter. Ini mengurangi request yang tidak diperlukan dan beban
   server, serta membantu hasil pencarian tetap relevan dengan input terbaru.

2. `fetch()` mengembalikan sebuah `Promise`, karena respons jaringan tidak
   langsung tersedia. `await` menunggu Promise tersebut selesai sebelum
   menjalankan baris berikutnya, sehingga respons dapat diperiksa dan isi JSON
   dapat dibaca pada urutan yang benar. Tanpa `await`, kode langsung berjalan
   dengan nilai Promise, bukan respons yang sudah diterima. Kita tetap dapat
   menangani Promise tanpa `await` dengan `.then()`, tetapi jika Promise tidak
   ditangani, data belum dapat digunakan dan error asinkron dapat terlewat.

3. **Cross-Site Scripting (XSS)** adalah serangan ketika konten yang dikendalikan
   penyerang ditafsirkan browser sebagai kode aktif, misalnya JavaScript, lalu
   dijalankan pada halaman pengguna lain. Data dari AJAX diterima sebagai nilai
   JavaScript dan tidak otomatis melalui proses auto-escaping template Django.
   Jika nilai itu langsung dimasukkan ke halaman dengan `innerHTML`, markup atau
   skrip berbahaya dapat ditafsirkan oleh browser. Karena itu, teks sebaiknya
   ditampilkan melalui `textContent` atau di-escape sebelum dirender sebagai
   HTML. Template Django melakukan auto-escaping secara default, kecuali
   escaping tersebut sengaja dinonaktifkan.

**AI Disclosure:** Saya menggunakan AI sebagai asisten untuk mengimplementasikan endpoint dan antarmuka AJAX Interests, serta
menyusun tes. Saya menentukan bagian portofolio yang dikerjakan, memberikan
konteks hak akses Tugas 4, memilih pengerjaan bertahap agar tiap tahap dapat
ditinjau dan di-commit, serta meminta perubahan dan pemeriksaan lanjutan.
Verifikasi otomatis dilakukan dengan menjalankan tes Django dan pemeriksaan
halaman/API di lingkungan pengembangan. Saya bertanggung jawab untuk meninjau
hasil akhir dan memastikan penjelasan tugas ini sesuai dengan pemahaman saya.


### Tugas 6

1. **Konsep REST, JSON, dan Perbedaan PUT vs PATCH:**
   - **REST (Representational State Transfer)** adalah gaya arsitektur perancangan web API yang memperlakukan data sebagai *resource* yang diidentifikasi secara unik melalui URI (endpoint), menggunakan metode HTTP standar (GET, POST, PUT, PATCH, DELETE) untuk menyatakan tindakan tanpa menulis kata kerja di URL, dan bersifat *stateless* (setiap request membawa seluruh konteks yang diperlukan tanpa bergantung pada sesi stateful di memori server).
   - Mengembalikan data dalam format JSON saja **belum cukup** untuk menyebut sebuah API sebagai RESTful. JSON hanyalah format serialisasi/representasi data. Suatu API tidak RESTful jika URL-nya menyertakan aksi (misalnya `POST /interest/add/` atau `POST /interest/<id>/delete/`), menggunakan method HTTP yang tidak sesuai (misal menggunakan GET untuk menghapus data), atau melanggar kontrak statelessness.
   - **Perbedaan PUT dan PATCH:**
     - **PUT** melakukan penggantian resource secara menyeluruh (*full replacement*). Klien wajib mengirimkan seluruh representasi lengkap dari field resource yang dibutuhkan. Jika ada atribut wajib yang dihilangkan, request akan ditolak (400 Bad Request).
       *Contoh penggunaan:* Memperbarui seluruh data interest pada endpoint `PUT /api/v1/interests/<uuid>/` dengan mengirimkan payload lengkap: `{"title": "Baking", "description": "Sourdough and pastry baking", "since": 2021}`.
     - **PATCH** melakukan pembaruan parsial (*partial modification*). Klien hanya perlu mengirimkan field-field yang ingin diubah saja, sementara field lainnya tetap mempertahankan nilai yang tersimpan sebelumnya.
       *Contoh penggunaan:* Mengoreksi tahun mulai interest tanpa mengubah judul dan deskripsi pada endpoint `PATCH /api/v1/interests/<uuid>/` dengan payload: `{"since": 2022}`.

2. **Peran Serializer pada Django REST Framework:**
   - **Peran Serializer:** Bekerja dua arah (*bidirectional*). Pada proses serialisasi (*read/outgoing*), serializer menerjemahkan instance model Django atau QuerySet menjadi tipe data primitif Python yang dapat dirender menjadi JSON oleh renderer DRF. Pada proses deserialisasi (*write/incoming*), serializer memvalidasi data masukan dari request klien, membersihkan input dari tag berbahaya (`strip_tags`), memetakan error secara terperinci per-field, dan menyimpannya ke database via `.save()`.
   - **Keuntungan dibandingkan merakit dictionary manual dengan `JsonResponse`:**
     - *Validasi Terpusat dan Otomatis:* Validasi tipe data, batasan karakter, keunikan, serta validasi kustom (`validate_<field>`) ditangani secara deklaratif dalam satu berkas terpusat, alih-alih menulis blok `if-else` berulang di setiap fungsi view.
     - *Penanganan Error Terstruktur:* Serializer otomatis memetakan pesan error validasi ke format standar (`{"field": ["pesan error"]}`) dengan status HTTP yang tepat (400 Bad Request) melalui `is_valid(raise_exception=True)`.
     - *Integrasi ORM yang Efisien:* Mengurangi duplikasi kode (*DRY principle*). Pembuatan objek baru (`.create()`) maupun pembaruan instance (`.update()`) ditangani otomatis oleh `ModelSerializer`.
     - *Kalkulasi Data Terisolasi:* Field kalkulasi dinamis (seperti status `is_starred` dan `star_count`) dapat dibuat rapi melalui `SerializerMethodField` dengan memanfaatkan `context={"request": request}` tanpa mencemari logika view utama.

3. **Perbedaan Autentikasi vs Otorisasi dan Alasan Pemeriksaan di Server:**
   - **Autentikasi (Authentication)** menjawab identitas pengguna: *"Siapa kamu?"*. Proses ini memverifikasi kredensial pengguna (misalnya via cookie sesi Django pada `SessionAuthentication` atau token) dan mengisi objek `request.user`.
   - **Otorisasi (Authorization/Permissions)** menjawab hak akses pengguna: *"Apa yang boleh kamu lakukan?"*. Proses ini menentukan apakah pengguna yang telah terautentikasi (atau anonim) memiliki wewenang untuk menjalankan tindakan tertentu pada resource terkait (misalnya apakah user berhak melakukan `DELETE` atau `PATCH`).
   - **Mengapa hak akses harus diperiksa di server (permission class):**
     - Menyembunyikan tombol atau link di template frontend hanyalah elemen kenyamanan antarmuka (*UI affordance*) agar pengguna tidak melihat tombol yang tidak relevan.
     - Klien browser sepenuhnya berada di bawah kendali pengguna. Siapa pun dapat membuka Developer Tools, cURL, Postman, atau membuat script JavaScript untuk menembak request HTTP langsung ke endpoint URL tanpa melalui antarmuka web.
     - Jika pemeriksaan hak akses tidak dilakukan di server menggunakan permission class, penyerang atau pengguna biasa dapat mengubah atau menghapus data milik orang lain hanya dengan mengirimkan request `DELETE` atau `PUT` langsung ke API. Server adalah satu-satunya sumber kebenaran (*single source of truth*) yang menjamin keamanan data.

4. **CSRF Protection pada SessionAuthentication dan Keterbatasan `force_authenticate`:**
   - **Mengapa permintaan tulis memerlukan token CSRF pada `SessionAuthentication`:**
     - `SessionAuthentication` memanfaatkan cookie browser (`sessionid`) untuk mengidentifikasi pengguna. Browser secara otomatis menyertakan cookie ini pada setiap request ke origin yang sama, bahkan jika request tersebut dipicu oleh situs jahat pihak ketiga (serangan *Cross-Site Request Forgery*).
     - Token CSRF (`X-CSRFToken`) adalah nilai acak rahasia yang hanya dapat diakses oleh skrip yang berasal dari domain yang sama (*Same-Origin Policy*). Dengan mewajibkan header `X-CSRFToken` pada setiap request yang mengubah status (POST, PUT, PATCH, DELETE), server dapat memastikan bahwa permintaan tersebut benar-benar diinisiasi secara sadar oleh frontend aplikasi kita, bukan manipulasi dari situs eksternal.
   - **Mengapa `force_authenticate` tidak cukup untuk membuktikan perlindungan CSRF:**
     - `force_authenticate` adalah jalan pintas pengujian (*test convenience*) yang disediakan DRF untuk langsung menempelkan instance `User` ke atribut `request.user` pada mock request tanpa melalui middleware autentikasi dan penanganan cookie Django yang sebenarnya.
     - Karena tidak melewati middleware Django, seluruh alur verifikasi `CsrfViewMiddleware` dilewati (*bypassed*).
     - Untuk membuktikan bahwa mekanisme proteksi CSRF bekerja secara nyata, pengujian harus menggunakan `APIClient(enforce_csrf_checks=True)` dan menjalankan proses login sesungguhnya (`client.login(...)`). Hal ini memvalidasi bahwa permintaan tanpa header CSRF token akan ditolak dengan status HTTP 403 Forbidden, sementara permintaan yang menyertakan token CSRF yang valid akan diterima dan diproses dengan sukses.

---

**AI Disclosure:**
Proyek ini dikembangkan dengan bantuan AI (Antigravity Assistant dengan model Gemini 3.8 Flash). Bantuan AI digunakan untuk:
1. Menyusun arsitektur endpoint Django REST Framework pada model `Interest` (meliputi `InterestSerializer`, permission class `IsPortfolioOwnerOrEditorOrReadOnly`, dan fungsi API views).
2. Membangun modal interaktif Edit Interest berbasis AJAX/Fetch API pada `templates/interest.html` dan `static/js/interests.js` dengan integrasi CSRF token dan sanitasi error via toast.
3. Menyusun unit test komprehensif berbasis `APITestCase` yang menguji keempat peran akses pengguna, integritas database, dan pengujian proteksi CSRF.

*Analisis Kritis & Perbaikan Manual:*
AI memiliki keterbatasan dalam memahami urutan siklus hidup inisialisasi Django (`AppConfig.ready()`). Sebelumnya, terdapat pemanggilan database query langsung di `main/apps.py` saat aplikasi dimuat yang memicu error fatal `OperationalError: no such table: auth_group` pada database baru atau saat eksekusi migrasi. Perbaikan manual dilakukan dengan memindahkan inisialisasi grup dan hak akses ke signal `post_migrate` serta menambahkan perlindungan agar tidak memicu `IntegrityError` (konflik grup duplikat) saat test runner Django mengeksekusi test suite. Seluruh hasil kode dan unit test diverifikasi secara mandiri melalui perintah `python manage.py test main`.
