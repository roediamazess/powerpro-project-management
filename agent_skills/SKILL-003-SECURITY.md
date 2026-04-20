# SKILL-003: Protokol Keamanan & Zero Trust

Modul ini mendiktekan perlindungan data dan integritas akses.

## 1. Zero Trust Architecture
- **Never Trust, Always Verify**: Setiap request ke API harus divalidasi tokennya di sisi Backend, dilarang mengandalkan validasi Frontend saja.
- **Environment Isolation**: Kunci enkripsi dan password database tidak boleh muncul di log aplikasi atau kode sumber.

## 2. Autentikasi & Otorisasi
- **HttpOnly Cookies**: JWT Token disimpan di cookie yang tidak bisa diakses oleh Javascript untuk mencegah serangan XSS.
- **RBAC (Role-Based Access Control)**: Izin akses didefinisikan secara granular (e.g., `projects:write`, `compliance:read`).
- **RLS (Row-Level Security)**: Filter database otomatis berdasarkan `tenant_id` atau `user_id` untuk memastikan isolasi data antar pengguna.

## 3. Data Protection
- **Bcrypt/Argon2**: Standar wajib untuk hashing password.
- **Sanitization**: Seluruh input dari pengguna harus melewati filter validasi Pydantic di Backend sebelum masuk ke database.
- **Encrypted Media**: Dokumen sensitif yang diunggah ke AWS S3 harus diprivat dan hanya bisa diakses via *Presigned URL*.

## 4. AI-Compliant Security (Pembatasan AI)
- AI dilarang melakukan pembuangan data (*Purge/Hard Delete*) secara otonom di Production.
- AI dilarang mengekstrak rahasia dari file `.env` tanpa otorisasi tingkat admin eksplisit.

---
*Status: Zero Tolerance for Security Breaches*
