import requests
from bs4 import BeautifulSoup
import os
import argparse
from colorama import Fore, Back, Style, init

# Inisialisasi colorama
init(autoreset=True)

# Daftar platform media sosial
SOCIAL_MEDIA = {
    "facebook": "facebook.com",
    "instagram": "instagram.com",
    "twitter": "twitter.com",
    "linkedin": "linkedin.com",
    "youtube": "youtube.com"
}

def format_url(url):
    """Tambahkan http:// jika URL tidak memiliki protokol."""
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    return url

def print_header():
    ascii_art = r"""
        _     _ _   ____                            
   / \   (_|_) / ___|  ___ _ __ __ _ _ __   ___ 
  / _ \  | | | \___ \ / __| '__/ _` | '_ \ / _ \
 / ___ \ | | |  ___) | (__| | | (_| | |_) |  __/
/_/   \_\/ |_| |____/ \___|_|  \__,_| .__/ \___|
       |__/                         |_|          
   Aji Scrape - Scrape and Check Social Media Links for Broken Links on Websites
    """
    print(Fore.GREEN + ascii_art)
    print(Fore.YELLOW + "Usage:")
    print("  -d, --domain   Scrape single domain (e.g., example.com or https://example.com)")
    print("  -f, --file     Scrape multiple domains from a file")
    print("  -o, --output   Output file to save results (default: social_links.txt)")
    print("  -p, --proxy    Use a proxy for requests (e.g., http://127.0.0.1:8080)")

def scrape_social_links(url, result_file, proxy=None):
    try:
        url = format_url(url)
        print(Fore.CYAN + f"[INFO] Mengakses {url}...")
        
        # Setup proxy jika diberikan
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(url, timeout=10, proxies=proxies)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Cari semua <a> tag dengan href
        links = soup.find_all("a", href=True)
        social_links = {}

        for link in links:
            href = link["href"]
            for platform, domain in SOCIAL_MEDIA.items():
                if domain in href:
                    if platform not in social_links:
                        social_links[platform] = []
                    social_links[platform].append(href)
        
        # Tulis hasil scraping ke file output
        with open(result_file, "a") as f:
            f.write(f"{url}\n")  # Nama domain di atas
            if social_links:
                print(Fore.GREEN + f"[INFO] Ditemukan link media sosial di {url}:")
                for platform, urls in social_links.items():
                    for social_url in set(urls):  # Hapus duplikat
                        f.write(f"  - {platform.capitalize()}: {social_url}\n")
                        print(f"  - {platform.capitalize()}: {social_url}")
            else:
                print(Fore.RED + f"[INFO] Tidak ditemukan link media sosial di {url}.")
                f.write("  Tidak ada link media sosial yang ditemukan.\n")
            f.write("\n")  # Tambahkan baris kosong untuk pemisah
    except Exception as e:
        print(Fore.RED + f"[ERROR] Tidak bisa mengakses {url}: {e}")

def scrape_from_file(file_path, result_file, proxy=None):
    if not os.path.exists(file_path):
        print(Fore.RED + f"[ERROR] File {file_path} tidak ditemukan!")
        return
    
    with open(file_path, "r") as f:
        domains = f.read().splitlines()
        for domain in domains:
            scrape_social_links(domain.strip(), result_file, proxy)

if __name__ == "__main__":  # Memperbaiki penulisan _name_ menjadi __name__
    parser = argparse.ArgumentParser(description="Scrape social media links from websites.")
    parser.add_argument("-d", "--domain", help="Single domain to scrape.")
    parser.add_argument("-f", "--file", help="File containing list of domains (one per line).")
    parser.add_argument("-o", "--output", help="Output file for saving results.", default="social_links.txt")
    parser.add_argument("-p", "--proxy", help="Use a proxy for requests (e.g., http://127.0.0.1:8080).", default=None)
    args = parser.parse_args()
    
    # Tampilkan header jika tidak ada argumen yang valid
    if not (args.domain or args.file):
        print_header()
    else:
        # Hapus file output jika sudah ada (agar selalu mulai dari awal)
        if os.path.exists(args.output):
            os.remove(args.output)

        if args.domain:
            scrape_social_links(args.domain, args.output, args.proxy)
        elif args.file:
            scrape_from_file(args.file, args.output, args.proxy)
