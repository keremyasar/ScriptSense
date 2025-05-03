import os
import re
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

# Klasör yolları
stemmed_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\stemmed_dialogues"
lemmatized_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\lemmatized_dialogues"
zipf_stemmed_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\zipf_stemmed"
zipf_lemmatized_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\zipf_lemmatized"

# Eğer klasörler yoksa oluştur
for folder in [zipf_stemmed_folder, zipf_lemmatized_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def preprocess_text(text):
    """Metni temizle ve kelimeleri çıkar."""
    text = text.lower()  # Küçük harfe çevir
    text = re.sub(r'[^a-zA-Zğüşıöç ]+', '', text)  # Özel karakterleri kaldır
    words = text.split()  # Kelimeleri ayır
    return words

def generate_zipf_graph(input_folder, output_folder):
    """Belirtilen klasördeki tüm dosyalar için Zipf yasası grafikleri oluştur."""
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(input_folder, file_name)
            plot_filename = os.path.join(output_folder, f"{file_name.replace('.txt', '_zipf.png')}")

            # Eğer dosya zaten varsa, işlemi atla
            if os.path.exists(plot_filename):
                print(f"Grafik zaten mevcut, atlanıyor: {plot_filename}")
                continue

            # Dosyayı oku
            with open(file_path, "r", encoding="utf-8-sig", errors="ignore") as f:
                text = f.read()

            # Metni temizle
            words = preprocess_text(text)

            # Kelime frekanslarını hesapla
            word_counts = Counter(words)

            # Zipf yasasına göre sıralı frekansları al
            sorted_counts = sorted(word_counts.values(), reverse=True)

            # Log-log ölçekleme için verileri hazırla
            ranks = np.arange(1, len(sorted_counts) + 1)
            frequencies = np.array(sorted_counts)

            # Log-log grafiği çiz
            plt.figure(figsize=(8, 6), dpi=100)
            plt.loglog(ranks, frequencies, marker="o", linestyle="none", label=file_name)
            plt.xlabel("Kelime Sırası")
            plt.ylabel("Frekans")
            plt.title(f"Zipf Yasası - {file_name}")
            plt.legend()
            plt.grid()

            # Grafik dosyasını belirlenen klasöre kaydet
            plt.savefig(plot_filename)
            plt.close()  # Belleği temizle

            print(f"Grafik başarıyla kaydedildi: {plot_filename}")

# Stemmed verileri için Zipf yasası grafikleri oluştur
generate_zipf_graph(stemmed_folder, zipf_stemmed_folder)

# Lemmatized verileri için Zipf yasası grafikleri oluştur
generate_zipf_graph(lemmatized_folder, zipf_lemmatized_folder)
