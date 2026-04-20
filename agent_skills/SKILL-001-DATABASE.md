# SKILL-001: Standar Arsitektur Database (PostgreSQL)

Modul ini mendiktekan bagaimana data harus disimpan, dikelola, dan bermigrasi.

## 1. Konvensi Penamaan (Naming Convention)
- **Tabel**: Jamak (*Plural*), huruf kecil, snake_case (e.g., `partners`, `project_pics`, `compliance_entries`).
- **Kolom**: Tunggal (*Singular*), snake_case (e.g., `partner_id`, `created_at`).
- **Primary Keys**: Selalu menggunakan **UUID** v4 untuk skalabilitas dan keamanan ID di URL.
- **Foreign Keys**: Harus eksplisit dengan relasi `ON DELETE RESTRICT` (untuk mencegah pemutusan relasi secara tidak sengaja) atau `ON DELETE CASCADE` (hanya untuk tabel child kecil).

## 2. Manajemen Migrasi (Alembic)
- **Alembic Only**: Dilarang membuat tabel atau mengubah kolom lewat SQL query manual di server Production.
- **Readable Versions**: Nama file migrasi harus deskriptif (e.g., `20240419_add_audit_log_payloads`).

## 3. Sistem Soft-Delete & Audit
- **Soft Delete**: Wajib ada kolom `is_deleted` (Boolean) dan `deleted_at`. AI harus otomatis menambahkan filter `is_deleted = False` pada query default.
- **Audit Logs**: Setiap mutasi (INSERT, UPDATE) harus memicu middleware untuk mencatat ke tabel `system_audit_logs`.

## 4. Performa (Indexing)
- **B-Tree Indexes**: Wajib ditambahkan pada kolom yang sering difilter oleh AG Grid (e.g., `status`, `assigned_to`, `due_date`).
- **Composite Indexes**: Dibangun seiring kebutuhan filtering kompleks pada dashboard.

---
*Status: Strict Enforcement*
