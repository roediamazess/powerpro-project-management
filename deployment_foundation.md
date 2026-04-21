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

## 11. Aturan Teknis AG Grid v35 (Critical — Jangan Dilanggar)

AG Grid versi 35 (yang digunakan proyek ini) memiliki **perubahan API yang bersifat breaking change** dibandingkan versi sebelumnya. Semua pengembangan yang melibatkan AG Grid **WAJIB** mengikuti standar berikut:

### 11.1 Quick Filter (Pencarian Global)

**❌ API Lama (Dihapus di v35 — JANGAN DIGUNAKAN):**
```javascript
// SALAH — setQuickFilter() sudah tidak ada di v35
gridApi.setQuickFilter('teks pencarian')
```

**✅ API Baru yang Benar (v35):**
```javascript
// BENAR — gunakan setGridOption
gridApi.setGridOption('quickFilterText', 'teks pencarian')
```

### 11.2 Pendaftaran Module Wajib

Quick Filter **TIDAK AKAN AKTIF** tanpa mendaftarkan `QuickFilterModule`. Wajib ada di `ModuleRegistry`:
```typescript
import { QuickFilterModule } from 'ag-grid-community'

ModuleRegistry.registerModules([
  ClientSideRowModelModule,
  QuickFilterModule, // ← WAJIB ADA untuk fitur pencarian global
  // ... modul lain
])
```

### 11.3 Integrasi Global Search dengan Pinia (Vue 3)

Pola standar untuk menghubungkan pencarian global dari header ke tabel AG Grid:

1. **State** — Simpan di `UIStore` (`frontend/src/store/ui.ts`)
2. **Trigger** — Gunakan `storeToRefs` + `computed` di View
3. **Propagasi** — Panggil `gridApi.setGridOption` via `watch` di `AppGrid.vue`

```typescript
// Di AppGrid.vue
watch(() => props.quickFilterText, (newVal) => {
  if (gridApi.value) {
    gridApi.value.setGridOption('quickFilterText', newVal ?? '')
  }
})
```

### 11.4 Search Context Integration
Informasi hasil pencarian tidak lagi diletakkan pada badge terpisah di samping kolom search untuk menghindari redundansi visual. Sebaliknya, hasil pencarian harus langsung tercermin pada **Tab Status** yang aktif.

**✅ Standar Implementasi:**
1. **Single Source of Truth**: Angka jumlah data hanya muncul di dalam komponen Tab.
2. **Logic Integration**: State `gridResultCount` tetap dipertahankan untuk menyuplai data ke Tab, namun visualisasinya dipusatkan pada badge internal Tab.
3. **Clean UI Policy**: Header harus tetap bersih dan fokus pada fungsionalitas pencarian tanpa elemen dekoratif tambahan yang berulang.

### 11.5 Status-Based Navigation Tabs (dengan Integrated Counter)
Modul utama wajib memiliki navigasi Tab yang menggabungkan kategori status dengan jumlah data yang relevan secara real-time.

**✅ Standar Visual & Fungsi:**
1. **Integrated Counter**: Setiap Tab wajib menampilkan angka jumlah baris (misal: `Progress 12`). Angka ini harus bereaksi terhadap *quick filter* pencarian.
2. **Logic Sync**: Gunakan hasil dari `api.getDisplayedRowCount()` yang dikirim via event `filterChanged` oleh `AppGrid`.
3. **Active State**: Tab aktif menggunakan **Gradient Background** (Cyan-to-Emerald/Teal) untuk menegaskan konteks yang sedang dilihat pengguna.

**✅ Pengelompokan Standar:**
- **Preparation**: (Tentative, Scheduled)
- **Progress**: (Running)
- **Documentation**: (Document, Document-Check)
- **Done**: (Done)
- **X**: (Cancelled, Rejected)
- **All**: (Semua Status)

**✅ Standar Visual:**
- Gunakan efek **Glassmorphism** pada kontainer tab.
- Tab aktif menggunakan **Gradient Background** (Cyan-to-Emerald) dengan teks putih.
- Sertakan **Counter Badge** kecil di dalam tab yang aktif untuk menunjukkan sisa beban kerja di status tersebut.

### 11.6 Dark Mode Header Styling (AG Grid)

Header AG Grid di dark mode **harus menggunakan nilai berikut** agar teks terbaca dengan kontras yang baik. Gunakan CSS override dengan spesifisitas tinggi:

```css
/* Wajib — Header background dan teks */
.dark.ag-theme-alpine {
  --ag-header-background-color: #0f1f3d !important; /* Biru navy dalam */
  --ag-header-foreground-color: #e2e8f0 !important; /* Putih cerah */
}

/* Wajib — Override eksplisit agar tidak tertimpa AG Grid */
.dark.ag-theme-alpine .ag-header {
  background-color: #0f1f3d !important;
  border-bottom: 2px solid rgba(6, 182, 212, 0.3) !important; /* Garis aksen cyan */
}

.dark.ag-theme-alpine .ag-header-cell-text {
  color: #e2e8f0 !important;
  font-weight: 700 !important;
  font-size: 11px !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
}

.dark.ag-theme-alpine .ag-icon {
  color: #64748b !important; /* Icon filter tetap halus */
}
```

**Nilai yang DILARANG digunakan di dark mode:**
- `--ag-header-foreground-color: #94a3b8` → terlalu redup, tidak terbaca
- `--ag-header-background-color: #1e293b` → terlalu mirip dengan row body

### 11.5 Vertical Column Separator (Garis Pemisah Antar Kolom)

AG Grid **tidak** menampilkan garis vertikal antar kolom secara default, kecuali pada kolom yang di-`pinned`. Menggunakan CSS variable saja (`--ag-cell-horizontal-border`, dll.) **tidak cukup** — harus menggunakan CSS selector langsung dengan `!important`.

**✅ Cara yang Benar:**
```css
/* Light Mode */
.ag-theme-alpine .ag-cell {
  border-right: 1px solid #e2e8f0 !important;
}
.ag-theme-alpine .ag-header-cell {
  border-right: 1px solid #cbd5e1 !important;
}

/* Dark Mode */
.dark.ag-theme-alpine .ag-cell {
  border-right: 1px solid rgba(30, 41, 59, 0.9) !important;
}
.dark.ag-theme-alpine .ag-header-cell {
  border-right: 1px solid rgba(99, 182, 255, 0.12) !important;
}
```

**❌ JANGAN gunakan pendekatan ini (tidak efektif di v35):**
```css
/* CSS variable saja tidak cukup untuk mengaktifkan border sel */
--ag-cell-horizontal-border: solid #e2e8f0;
```

### 11.6 Row Selection & Highlight (Klik Satu Baris)

Untuk menampilkan highlight baris saat diklik, AG Grid v35 memerlukan `RowSelectionModule` yang harus didaftarkan secara eksplisit. Tanpa modul ini, `api.deselectAll()` dan `node.setSelected()` akan gagal diam-diam tanpa error yang jelas.

**✅ Pendaftaran Module Wajib:**
```typescript
import { RowSelectionModule } from 'ag-grid-community'

ModuleRegistry.registerModules([
  ClientSideRowModelModule,
  QuickFilterModule,
  RowSelectionModule, // ← WAJIB untuk highlight baris
  // ... modul lain
])
```

**✅ Cara Mengaktifkan Highlight via `node.setSelected()`:**
```typescript
// Di AppGrid.vue — paling reliabel, tidak bergantung pada prop rowSelection
const onRowClicked = (params: any) => {
  params.api.deselectAll()       // Hapus seleksi sebelumnya
  params.node.setSelected(true)  // Pilih baris yang diklik
  emit('rowClicked', params)
}
```

Dan tambahkan di template:
```html
<ag-grid-vue
  rowSelection="single"
  :suppressCellFocus="true"
  @row-clicked="onRowClicked"
  ...
/>
```

**✅ CSS Highlight & Hover — Light & Dark Mode:**
AG Grid v35 dapat menimpa warna secara internal melalui default root variables, sehingga hover dan seleksi *membutuhkan* penargetan pseudo-class dan `.ag-cell` secara eksplisit dengan `!important`. Desain menggunakan palet warna yang premium dan lembut.

```css
/* --- LIGHT MODE --- */
/* Hover: Biru sangat lembut (#eff6ff / tailwind blue-50) */
.ag-theme-alpine .ag-row-hover:not(.ag-row-selected) {
  background-color: #eff6ff !important;
}
.ag-theme-alpine .ag-row-hover:not(.ag-row-selected) .ag-cell {
  background-color: #eff6ff !important;
}

/* Selected: Biru terang penegas (#bfdbfe / tailwind blue-200) */
.ag-theme-alpine .ag-row-selected .ag-cell {
  background-color: #bfdbfe !important;
}

/* --- DARK MODE --- */
/* Hover: Biru Navy Pudar (#162033) */
.dark.ag-theme-alpine .ag-row-hover:not(.ag-row-selected) {
  background-color: #162033 !important;
}
.dark.ag-theme-alpine .ag-row-hover:not(.ag-row-selected) .ag-cell {
  background-color: #162033 !important;
}

/* Selected: Biru Navy Dalam (#1e3a5f) */
.dark.ag-theme-alpine .ag-row-selected {
  background-color: #1e3a5f !important;
}
.dark.ag-theme-alpine .ag-row-selected .ag-cell {
  background-color: #1e3a5f !important;
  color: #f1f5f9 !important;
}
```

**⚠️ Perhatian Dark Mode:**
Jika dark mode memiliki rule `.ag-cell { background-color: #0f172a !important }`, rule `!important` ini akan menimpa warna selected. Solusinya: **hapus `!important`** dari rule default `.ag-cell` dan gunakan selector yang lebih spesifik untuk selected state.

**❌ JANGAN gunakan `!important` pada `.ag-row` atau `.ag-cell` di dark mode secara global:**
```css
/* SALAH — akan memblokir semua highlight */
.dark.ag-theme-alpine .ag-row, .dark.ag-theme-alpine .ag-cell {
  background-color: #0f172a !important; /* !important ini akan menimpa selected row */
}
```

### 11.7 UI Standardization: Action Buttons

Untuk menjaga konsistensi pada tombol aksi utama di setiap halaman (contoh: *Add Project*, *Add Partner*), tombol dengan kelas dasar `.btn-primary` mungkin akan merespons lebar kontainernya secara tak terduga atau terlalu rapat secara padding horizontal.

Gunakan standar utilitas berikut untuk memastikan rasio komponen Glassmorphism yang sempurna (tidak membetot atau terlalu mepet):
```html
<!-- STANDAR: Gunakan !w-auto dan px-8 (atau padding eksplisit lain) -->
<button class="btn-primary !w-auto px-8 ...">
  Add Project
</button>
```

### 11.8 Layout Standardization: Sticky Header & Internal Grid Scroll

Untuk aplikasi enterprise sejati (khususnya yang menyajikan Data Grid kompleks setinggi layar), **Pengguliran (Scrolling) tingkat Page/Root harus dihentikan**. Komponen Navbar, Header Halaman, dan Tombol-tombol navigasi harus beku (sticky) pada tempatnya. Hanya "Grid Body" yang murni menggulir isinya sendiri.

Gunakan standar hierarki DOM berikut di setiap modul utama untuk menyajikan interaktivitas ala *Desktop App*:

1.  **MainLayout**: Di tingkat root/routing, kunci layar agar tetap sebatas viewport.
    ```html
    <div class="h-screen flex flex-col overflow-hidden"> ... </div>
    ```

2.  **View Components (ex: PartnerListView)**: Pastikan Header bersifat statis (`flex-none`), sedangkan Kontainer Tabel meregang elastis (`flex-1 min-h-0`). **Standar Orientasi Header**: Grup Tombol Aksi berada di sisi **Kiri**, dan Judul Halaman berada di sisi **Kanan** (dengan properti `text-right`).
    ```html
    <template>
      <div class="h-full flex flex-col space-y-4 pb-2" v-auto-animate>
        <!-- STATIS: Header Layout Terstandarisasi -->
        <div class="flex-none flex items-center justify-between">
          
          <!-- KIRI: Aksi Utama (Add di kiri, Refresh, lalu Local Search) -->
          <div class="flex items-center gap-3">
            <button class="btn-primary !w-auto px-8 ...">Add Data</button>
            <button class="p-3 glass rounded-xl ...">Refresh</button>
            
            <!-- Local Search (Terkait ke AG Grid quickFilterText) -->
            <div class="relative group ml-2">
              <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-surface-500 group-focus-within:text-accent-cyan transition-colors z-10" />
              <input 
                v-model="currentSearch"
                type="text" 
                placeholder="Search..."
                class="w-48 xl:w-64 bg-surface-500/5 hover:bg-surface-500/10 border border-border-app hover:border-white/10 rounded-xl py-2 pl-9 pr-4 text-sm font-medium focus:outline-none focus:border-accent-cyan/50 focus:ring-1 focus:ring-accent-cyan/50 focus:bg-surface-900 transition-all shadow-inner relative"
              />
            </div>
          </div>
          
          <!-- KANAN: Text Title (text-right) -->
          <div class="text-right">
            <h1>Module Database</h1>
            <p>Management descriptive text...</p>
          </div>
        </div>

        <!-- ELASTIS: Hanya area Grid yang bergulir -->
        <div class="flex-1 min-h-0 relative">
          <AppGrid height="100%" :quickFilterText="currentSearch" /> 
        </div>
      </div>
    </template>
    ```

---

### 11.9 Floating Dynamic Dock & Global Navigation Standards

Aplikasi ini menggunakan pola **Floating Dynamic Dock** di bagian atas untuk navigasi utama. Berikut adalah standar konstruksinya:

1.  **Navigasi Vertikal (Center)**:
    Gunakan `flex-col` untuk menumpuk Icon di atas Label. Label harus menggunakan font yang sangat padat (`font-black`), ukuran kecil (`text-[9px]`), dan huruf kapital (`uppercase`).
    ```html
    <router-link class="flex flex-col items-center gap-1 ...">
      <Icon class="w-5 h-5" />
      <span class="font-black text-[9px] uppercase tracking-widest">MENU NAME</span>
    </router-link>
    ```

2.  **Identitas Brand (Left)**:
    Logo disematkan menggunakan file vektor (`.svg`) transparan di sisi kiri dock. Jangan gunakan background solid pada logo agar menyatu dengan efek `glassmorphism` Navbar.

3.  **Profile & User Management (Right)**:
    Integrasikan aksi user (Sign Out, Settings) ke dalam **Profile Dropdown**. Jangan gunakan tombol terpisah untuk Sign Out di bar utama. Dropdown harus memiliki transisi yang halus dan overlay klik di belakangnya untuk penutupan otomatis.

4.  **Standar Sinkronisasi Tema (Theme Syncing)**:
    -   Latar belakang root aplikasi harus menggunakan variabel semantik `bg-bg-app` (bukan hardcoded surface).
    -   **AG Grid**: Harus mendengarkan state `uiStore.theme` secara reaktif dan mengganti skema visual antara `ag-theme-alpine` (light) dan `ag-theme-alpine-dark` (dark) secara otomatis.
    -   Gunakan transisi CSS warna (`transition-colors duration-500`) pada elemen kontainer besar untuk efek pergantian tema yang sinematik.

5.  **Variabel CSS Semantik (`main.css`)**:
    Selalu petakan variabel `:root` sebagai warna **Light Mode** dan `.dark` sebagai warna **Dark Mode** untuk memastikan konsistensi transisi warna di seluruh aplikasi.

---

### 11.10 Standar Dark Mode Universal — Aturan Kritikal

Berikut adalah aturan yang WAJIB diikuti agar semua komponen bereaksi terhadap perubahan dark/light mode dengan benar:

**A. AG Grid Dark Mode (AppGrid.vue)**

> ⚠️ **KESALAHAN UMUM**: Mengganti kelas `ag-theme-alpine` dengan `ag-theme-alpine-dark` saat dark mode — ini mematikan selector dark yang sudah didefinisikan.

**Cara yang BENAR**: Gunakan selalu `ag-theme-alpine` sebagai kelas tetap, dan tambahkan `dark` secara kondisional ke container yang SAMA:
```html
<!-- ✅ BENAR — selector .dark.ag-theme-alpine akan match -->
<div
  class="ag-theme-alpine"
  :class="uiStore.theme === 'dark' ? 'dark border-surface-700/50' : 'border-surface-200'"
>
```
CSS selector dark mode di AppGrid.vue menggunakan `.dark.ag-theme-alpine { ... }` — kedua kelas harus hadir di elemen yang sama.

**B. Background Container — Gunakan CSS Variable, Bukan Tailwind Dark Classes**

Saat Tailwind production build melakukan purge, kelas `dark:bg-surface-900` yang dipakai secara kondisional bisa dihapus. Gunakan inline style dengan CSS variable sebagai solusi anti-purge:
```html
<!-- ✅ AMAN dari purge -->
<div :style="{ backgroundColor: 'var(--bg-app)' }">...</div>
<div :style="{ backgroundColor: 'var(--bg-card)' }">...</div>
```

**C. Safelist Tailwind untuk Dark Mode Classes**

Tambahkan kelas dark mode kritikal ke `safelist` di `tailwind.config.js` agar tidak di-purge:
```js
safelist: [
  'dark:bg-surface-900',
  'ag-theme-alpine-dark',
  'ag-theme-alpine',
]
```

**D. Teks & Border — Selalu Gunakan Variabel Semantik**

| ❌ Hindari | ✅ Gunakan |
|---|---|
| `text-surface-500` | `text-secondary` |
| `text-white` | `text-primary` |
| `border-surface-800/50` | `border-border-app` |
| `bg-surface-900` | `var(--bg-card)` atau `var(--bg-app)` |

---

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
