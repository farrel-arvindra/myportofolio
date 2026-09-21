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