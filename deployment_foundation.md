# Arsitektur & Landasan Deployment (Deployment Foundation) v2 (AI-Enhanced)

Dokumen ini berisi landasan arsitektur pengembangan, aturan standar operasional internal, dan rencana *deployment* sistem terotomatisasi untuk modul *Project Management, Partner Management, Timeboxing, dan Compliance*. Arsitektur versi terbaru (v2) ini didesain agar kompatibel 100% dan dapat disetir secara otonom oleh **AI Assistant (Google Antigravity Agent Skills)**.

## 1. Tech Stack Overview
| Layer | Teknologi Utama | Keterangan |
| :--- | :--- | :--- |
| **Backend** | Python / FastAPI | Dipilih karena performa tinggi, native async otomatis, dan validasi sintaks cerdas. Menggunakan **Gunicorn + Uvicorn workers** di produksi. |
| **Frontend** | Vue 3 (Composition API) + TypeScript | Skalabilitas tinggi memanajemen state. Terintegrasi **OpenAPI Codegen** untuk sinkronisasi tipe otomatis. |
| **UI/UX Desain**| Tailwind CSS + Komponen | Kombinasi HSL & Custom CSS responsif untuk menghasilkan aplikasi bertaraf premium/enterprise. |
| **Data Grid** | AG Grid | Merender data berskala masif dengan kalkulasi sisi Server (SSR) tanpa kendala. |
| **Database** | PostgreSQL + Alembic | Konvensi ERD ketat dengan manajemen migrasi skema berbasis versi (**Alembic**). |

---

## 2. Integrasi AI & Agent Skills (Google Antigravity)

Pada tingkat evolusi _Enterprise_, _Deployment_ bukan hanya sekadar mengunggah *code* ke *server*, tetapi memberdayakan AI agar memahami struktur arsitektur murni layaknya *SysOps Developer* sejati.

1.  **AI Modul Kecerdasan & Business Context (Agent Skills):** 
    Platform akan ditemani oleh file atau modul statis **Agent Skills**. Ini memastikan bahwa agen AI Antigravity selalu menguasai standar bisnis, *guideline* sistem (seperti cara sistem CRM kita bekerja, integritas audit log, dll), hingga standar *best-practice* tanpa harus dijelaskan berulang-ulang oleh manusia.
2.  **Autonomous SysOps / CI-CD Operator:** 
    Dengan *Agent Skills*, AI mampu memahami kerangka kerja arsitektur `Github Actions` dan `Docker Compose` secara absolut. AI dapat menganalisis *error log*, memecahkan *bottleneck* server, memulihkan data, dan melakukan _debugging_ lintas-_layer_ (Frontend -> Backend -> Database) murni melalui konteks bawaan yang dimilikinya.
3.  **Keamanan Berlapis (AI-Compliant Zero Trust):**
    Aturan *Agent Skills* secara spesifik melarang keras agen AI untuk mengeksekusi _hard-delete_ secara mandiri di Production, mengekspos kata sandi, atau membaca .env tanpa otorisasi. AI akan menyesuaikan intervensinya demi terjaganya protokol Zero-Trust.

---

## 3. Aspek Profesional (Maintainability & Standar Operasi)

1. **Sistem CI/CD & Pipeline (Otomatisasi Server Virtual):**
   * Metodologi *GitFlow* di atas repositori **GitHub** sebagai pusat _version control_.
   * *GitHub Actions* otomatis memicu proses *testing* (yang juga bisa di-review oleh AI) hingga *deployment* ke Production server secara *Zero-Downtime*.
2. **Sistem Jejak Rekam (Audit Trail & Anti-Fraud):**
   * Di tabel `system_audit_logs` (PostgreSQL), *middleware* FastAPI selalu menangkap perubahan data JSON `old_payload` ke `new_payload`. Rekam jejak ini tidak dapat dihapus, bahkan AI akan diinstruksikan selalu melewati fase interseptor ini lewat *Agent Skills*.
3. **Standar UI/UX Design System (Premium & Fluid):**
   * Tampilan UI dilengkapi *Dark Mode* mutlak, interaksi mikroskopis efek *Hover/Glassmorphism*, dan transisi pewarnaan yang mewah memanfaatkan Custom Tokens berbasis TailwindCSS. Desain tak mentah.

---

## 4. Struktur Data (1NF Normalized) Cerdas

*   **Authentication & RBAC**: `users`, `roles`, dan `tiers`. Autentikasi ketat; interaksi data secara otomatis dilimitasi sistem `Row-Level` oleh FastAPI berdasarkan *Tier* User.
*   **CRM / Partner Management**: Tabel utama `partners` dikawal bersama `partner_contacts`. AI mengintegrasikan wawasan relasi di antara keduanya ketika membuat pelaporan analitik.
*   **Project & Timeboxing Management**: Mengelola kolaborasi lewat tabel jembatan `project_pics`. Penerapan *Timeboxing* untuk `tasks` dipantau terpusat. Entitas *Foreign Key* tak pernah terputus secara barbar.
*   **Audit / Compliance System**: Struktur dinamis formulir multi level (`compliance_entry`). Memerlukan kecerdasan validasi interaktif.

---

## 5. Strategi Keamanan Mutlak (Secure - Zero Trust)

1.  **Proteksi Sesi:** Transmisi otomatis token otorisasi ke _HttpOnly Cookies_. Token API tidak akan pernah disuplai mentah di Frontend/LocalStorage.
2.  **Isolasi Konfigurasi:** Semua kredensial/rahasia produksi tidak akan terdokumentasi di *Git* dan selalu diproteksi dari AI publik via injeksi dinamis `.env`.
3.  **Role Limitation (Multi-RBAC):** Modifikasi, modifikasi silang, penghapusan tersembunyi bergradasi berdasarkan kekuasaan *tier* manajemen.

---

## 6. Operasional Kinerja Tinggi & Skalabilitas

1.  **Frontend Route Splitting (Vite):** Akselerasi awal. Beban _Javascript_ (seperti AG-Grid) dimuat perlahan seiring rutenya dijamah, membuat *Initial Load Time* terasa instan.
2.  **Redis In-Memory Caching (Backend):** Lookup Data diringankan lewat Redis supaya PostgreSQL luput dari *Query* konstan, memastikan tembakan Request merespons dalam kecepatan hitungan milidetik.
3.  **AG Grid Server-Side Filtering & B-Tree:** Menahan data jutaan baris supaya tak membuat tab *browser* *Freezing*. Dilaraskan oleh Indeks ganda tipe *B-Tree* otomatis di DBMS.

---

## 7. Ekstensibilitas Interaktif & Lanjutan (Background Tasks)

1.  **Pemroses Latar Belakang (Celery & Redis):** Ekspor masif Excel, notifikasi teguran email, kalkulasi *reporting*, dilepas secara gaib ke mesin latar belakang demi melindungi interaksi pengguna.
2.  **Sandi Pembaruan Real-Time (WebSockets):** Memicu pembaruan serentak. Indikator proyek, persentase keberhasilan otomatis kedap-kedip berkedip akurat di antarmuka komputer staf layaknya monitor bursa saham.
3.  **Penyimpanan Awan Media (AWS S3):** Lampiran pembuktian dialih-titipkan ke jaringan *bucket* luar server. Hard-disk server difokuskan murni mentenagai I/O _database_ saja.
4.  **Hukum Soft Delete Abadi:** Mutlak hukumnya dilarang menerapkan metode `DELETE SQL` demi kesucian integritas *Audit Logs*. Data *PostgreSQL* hanya dikenakan cap *is_deleted = true*.
5.  **Standardisasi Waktu Central (WIB):** Basis konfigurasi semua tabel `timestamp` dan *Cron-Job server* di-patri secara diktator menuju Waktu Indonesia Barat.

---

## 8. Manajemen Kelestarian & Evolusi Data (Alembic)
Untuk menghindari kerusakan data saat pengembangan fitur baru:
1.  **Versioning Skema:** Setiap perubahan kolom/tabel di pangkalan data wajib melalui **Alembic Migrations**. Dilarang mengubah skema secara manual via *Query Tool* di Production.
2.  **Integrasi AI Review:** AI (Agravity) diwajibkan memeriksa skrip migrasi untuk mendeteksi potensi kehilangan data (*Destructive Changes*) sebelum dijalankan.

## 9. Orchestrasi Server & Traffic Control (Nginx/Traefik)
Stabilitas akses diatur melalui lapisan proxy luar:
1.  **Reverse Proxy:** Menggunakan **Nginx** (atau Traefik) sebagai gerbang utama. Menangani terminasi SSL/TLS (Let's Encrypt), kompresi Gzip/Brotli, dan perlindungan header (CSP, HSTS).
2.  **SSL/TLS Mutlak:** Akses non-HTTPS akan dipaksa (*Redirect*) secara otomatis ke jalur aman.
3.  **Docker Profiles:** Menggunakan profil terpisah (`dev`, `staging`, `prod`) pada *Docker Compose* untuk memastikan *environment parity* yang konsisten.

## 10. Sinkronisasi Kontrak API (OpenAPI Codegen)
Menghilangkan celah ketidakcocokan data antara Frontend dan Backend:
1.  **Auto-Type Generation:** Menggunakan **OpenAPI Typescript Codegen**. Setiap kali ada perubahan skema Pydantic di FastAPI, AI akan men-*trigger* pembuatan ulang API Client di Vue 3 secara otomatis.
2.  **Zero-Drift Policy:** Menjamin data yang dikirim Backend selalu sesuai dengan harapan komponen Frontend tanpa pengecekan manual.

## 12. Quick-Start Produksi (Antigravity One-Click)

Untuk menjalankan sistem ini langsung di server produksi (VPS), ikuti instruksi berikut:

1.  **Persiapan Server**: Pastikan server memiliki `git`, `docker`, dan `docker-compose`.
2.  **Clone / Copy Project**: Pindahkan folder proyek ke server.
3.  **Eksekusi Otonom**:
    Jalankan perintah sakti berikut di root direktori:
    ```bash
    chmod +x deploy.sh && ./deploy.sh
    ```

Sistem akan secara otomatis:
- Membuat file `.env` dan `SECRET_KEY`.
- Membangun kontainer *High-Performance* (Gunicorn + Nginx).
- Menjalankan migrasi database ke versi terbaru.
- Mengaktifkan monitoring Sentry.

---
*Status: Production Ready v2.4 (Antigravity Certified)*
