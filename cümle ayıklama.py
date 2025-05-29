import os
import csv
import re
import random

def extract_random_meaningful_sentence(text):
    """ Metinden **rastgele anlamlı ve tek satırlık bir cümle** seçer. """
    sentences = text.split("\n")  # 🔹 Metni satır satır ayır
    filtered_sentences = [s.strip() for s in sentences if len(s.strip()) > 10 and re.search(r"[.?!]", s) and " " in s]  # 🔹 Anlamlı cümleleri filtrele
    
    return random.choice(filtered_sentences) if filtered_sentences else None  # 🔹 Rastgele bir cümle seç, yoksa None döndür

def extract_sentences_from_folder(folder_path, output_csv):
    """ Klasördeki tüm .txt dosyalarından **rastgele** anlamlı tek satırlık bir cümleyi çekip CSV'ye kaydeder. """
    data = []
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if file_name.endswith(".txt"):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()
                    sentence = extract_random_meaningful_sentence(text)  # ✅ Rastgele anlamlı tek satırlık cümleyi al
                    if sentence:
                        data.append([file_name, sentence])  # 🔹 Her dosya için **rastgele** bir cümle ekle
            except Exception as e:
                print(f"Hata oluştu ({file_name}): {e}")

    # CSV'yi kaydet
    with open(output_csv, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["document_id", "content"])
        writer.writerows(data)

# Kullanım
folder_path = "F:\\DOĞAL DİL\\scripts"
output_csv = "F:\\DOĞAL DİL\\output.csv"
extract_sentences_from_folder(folder_path, output_csv)
