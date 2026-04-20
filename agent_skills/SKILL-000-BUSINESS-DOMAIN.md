# SKILL-000: Konteks Bisnis & Terminologi Domain

Modul ini memberikan pemahaman mendalam tentang ekosistem operasional di mana The PowerPro diterapkan.

## 1. Domain Utama: Hospitality & Project Control
- **Partner Management**: Mengelola vendor, pemilik properti, dan kontraktor.
- **Project PIC**: Person In Charge. Seringkali melibatkan banyak pihak (Many-to-Many).
- **Compliance Entry**: Data bukti kepatuhan yang harus diverifikasi (misal: sanitasi, standar keamanan, inspeksi teknis).

## 2. Domain Industri: Modbus TCP & IoT
- **Modbus TCP**: Protokol komunikasi standar industri untuk perangkat (misal: kontrol suhu chiller hotel, sensor listrik, elevator).
- **Industrial Standards**: AI harus memahami konteks bahwa "Compliance" bisa berarti pemenuhan standar pembacaan register sensor secara otomatis.

## 3. Matriks Organisasi
- **Tiers**: Tingkat akses (misal: Tier 1 - Executive, Tier 2 - Manager, Tier 3 - Staff).
- **Row-Level Limit**: Aturan di mana Staff hanya bisa melihat data miliknya sendiri, sementara Manager bisa melihat agregat per departemen.

## 4. Pelaporan (Reporting)
- **Materialized Views**: Digunakan untuk agregat KPI yang berat. AI harus tahu bahwa data report mungkin memiliki delay sinkronisasi kecuali tombol "Rebuild" ditekan.
- **Audit Trails**: Bukan sekadar log aktivitas, tetapi bukti hukum (Legal Evidence) untuk kepatuhan industri.

---
*Gunakan konteks ini saat membuat endpoint API atau label UI.*
