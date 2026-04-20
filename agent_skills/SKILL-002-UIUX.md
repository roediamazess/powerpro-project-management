# SKILL-002: Standar UI/UX Design System (The PowerPro Style)

Modul ini mendiktekan estetika dan standar interaksi antarmuka pengguna.

## 1. Estetika Utama (Premium Look)
- **Tema**: Default Dark Mode yang elegan (Slate/Zinc).
- **Glassmorphism**: Gunakan `backdrop-blur` pada modal, sidebar, dan header dengan opasitas rendah.
- **Gradients**: Gunakan gradasi warna yang halus (bukan warna solid tajam) untuk indikator status.

## 2. AG Grid Standards (Modern Data Visualization)
- **Theme**: Gunakan tema `ag-theme-alpine-dark` dengan modifikasi CSS Tailwind untuk menyesuaikan dengan palet warna PowerPro.
- **Filtering**: Pastikan *Server-Side Filtering* dan *Sorting* aktif untuk tabel dengan data > 50 baris.
- **Cell Rendering**: Gunakan komponen kustom Vue 3 untuk sel yang kompleks (e.g., bar persentase, avatar PIC, badge status).

## 3. Komponen & State Management
- **Vue 3 Composition API**: Wajib menggunakan `<script setup>` dan TypeScript.
- **Pinia**: Digunakan untuk state global (Autentikasi, Pemberitahuan, Konteks User).
- **Lazy Loading**: Komponen berat (Chart, Grid) harus di-load secara dinamis untuk performa tinggi.

## 4. Micro-Animations
- **Transitions**: Setiap elemen modal dan sidebar saat terbuka/tertutup harus menggunakan transisi *ease-in-out*.
- **Interaction**: Gunakan efek *Pulse* halus untuk notifikasi yang membutuhkan perhatian segera.

---
*Dilarang menggunakan warna bawaan browser atau desain yang kaku.*
