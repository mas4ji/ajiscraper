# Ajiscrape - Scrape Social Media Links For Find Broken Link

Proyek ini berfungsi untuk scraping link media sosial dari situs web. Anda dapat menggunakannya untuk menemukan link ke profil media sosial seperti Facebook, Instagram, Twitter, LinkedIn, dan YouTube dari situs web.

## Fitur

- Scraping link media sosial dari satu situs web atau banyak situs web.
- Mendukung platform media sosial utama: Facebook, Instagram, Twitter, LinkedIn, YouTube.
- Output dapat disimpan dalam file teks.

## Instalasi Manual

Ikuti langkah-langkah berikut untuk menginstal dan menjalankan proyek ini secara manual:

1. **Clone repositori**:

    Pertama, clone repositori dari GitHub ke sistem lokal Anda dengan perintah berikut:

    ```bash
    git clone https://github.com/mas4ji/ajiscraper.git
    ```

2. **Masuk ke direktori proyek**:

    Setelah repositori di-clone, masuk ke direktori proyek dengan perintah:

    ```bash
    cd ajiscraper
    ```

3. **Instal dependensi**:

    Instal semua dependensi yang diperlukan dengan menjalankan:

    ```bash
    pip install -r requirements.txt
    ```

4. **Jalankan program**:

    Setelah semua dependensi terinstal, Anda dapat menjalankan program sesuai dengan instruksi di bagian penggunaan (usage).

---

## Penggunaan

Untuk menggunakan skrip ini, Anda bisa memilih untuk memproses satu domain atau beberapa domain sekaligus.

### Menggunakan satu domain:
```bash
python3 ajiscrape.py -d example.com -o hasil_scraping.txt
