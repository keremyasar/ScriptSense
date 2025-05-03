import requests
from bs4 import BeautifulSoup
import os
import time
import re
from urllib.parse import urljoin

base_url = "https://imsdb.com"
scripts_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\scripts"
os.makedirs(scripts_folder, exist_ok=True)

# Geçersiz karakterleri temizleme fonksiyonu
def safe_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

# HTML sayfasından soup alma fonksiyonu
def get_soup(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        else:
            print(f"[HATA] URL açılırken sorun yaşandı: {url}")
    except Exception as e:
        print(f"[EXCEPTION] {url} alınamadı: {e}")
    return None

def main():
    print("[+] IMSDb ana sayfa açılıyor...")
    soup = get_soup(base_url)
    if not soup:
        print("[X] Ana sayfa alınamadı.")
        return

    # All Scripts sayfasına git
    print("[+] 'All Scripts' sayfası aranıyor...")
    all_scripts_link = soup.find("a", string="ALL SCRIPTS")
    if not all_scripts_link:
        print("[X] 'All Scripts' bağlantısı bulunamadı.")
        return

    all_scripts_url = urljoin(base_url, all_scripts_link.get("href"))
    print(f"[+] All Scripts sayfasına gidiliyor: {all_scripts_url}")
    soup = get_soup(all_scripts_url)
    if not soup:
        print("[X] All Scripts sayfası alınamadı.")
        return

    # Film sayfalarının linklerini al
    print("[+] Film linkleri alınıyor...")
    film_links = soup.select("p a[href^='/Movie Scripts/']")
    if not film_links:
        print("[X] Film bağlantıları bulunamadı.")
        return

    print(f"[+] {len(film_links)} film bulundu. İndirme başlıyor...\n")

    for link in film_links:
        title = link.text.strip().replace(" ", "_").replace("/", "_")
        safe_title = safe_filename(title)  # Geçersiz karakterlerden temizle
        film_url = base_url + link.get("href")
        file_path = os.path.join(scripts_folder, f"{safe_title}.txt")

        # Daha önce indirilmişse, atla
        if os.path.exists(file_path):
            print(f"[✓] '{safe_title}' zaten mevcut, atlanıyor.\n")
            continue

        print(f"[>] {title} ({film_url})")

        # Film sayfasını aç
        film_soup = get_soup(film_url)
        if not film_soup:
            print(f"[!] {title} sayfası açılamadı.\n")
            continue

        # "Read Script" linkini bul
        read_script_link = film_soup.find("a", href=lambda x: x and x.startswith("/scripts/"))
        if not read_script_link:
            print(f"[!] '{title}' için 'Read Script' linki bulunamadı.\n")
            continue

        script_url = base_url + read_script_link.get("href")
        script_soup = get_soup(script_url)
        if not script_soup:
            print(f"[!] '{title}' için script sayfası açılamadı.\n")
            continue

        pre_tag = script_soup.find("td", class_="scrtext")
        if pre_tag:
            script_tag = pre_tag.find("pre")
            if script_tag:
                script_text = script_tag.get_text()
                # Script dosyasını kaydet
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(script_text)
                print(f"[✓] '{safe_title}' başarıyla kaydedildi.\n")
            else:
                print(f"[!] '{title}' için <pre> etiketi bulunamadı.\n")
        else:
            print(f"[!] '{title}' için senaryo içeriği bulunamadı.\n")

        time.sleep(1)  # Siteyi çok hızlı zorlamamak için bekleme

if __name__ == "__main__":
    main()
