import os
import re
import numpy as np
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

# 📌 **1️⃣ Metin temizleme fonksiyonu**
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Zğüşıöç ]+', '', text)
    return text.split()

# 📌 **2️⃣ Senaryo klasöründen dosyaları okuma**
def load_scripts(script_folder):
    scripts = {}
    for file_name in os.listdir(script_folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(script_folder, file_name)
            with open(file_path, "r", encoding="utf-8-sig") as f:
                scripts[file_name.replace(".txt", "")] = f.read()
    return scripts

# 📌 **3️⃣ Word2Vec modeli eğitme**
def train_word2vec(script_folder):
    scripts = load_scripts(script_folder)
    texts = [preprocess_text(scripts[film]) for film in scripts]
    model = Word2Vec(sentences=texts, vector_size=100, window=4, sg=1, workers=4)
    model.save("word2vec_film_model.model")  # Model dosyası kaydedildi
    return model, scripts

# 📌 **4️⃣ Her film için tek bir vektör hesaplama**
def film_vektoru_olustur(model, senaryo_metni):
    kelimeler = preprocess_text(senaryo_metni)
    vektörler = [model.wv[word] for word in kelimeler if word in model.wv]
    return np.mean(vektörler, axis=0) if vektörler else np.zeros(model.vector_size)

# 📌 **5️⃣ En benzer filmleri bulma**
def benzer_filmleri_bul(model, selected_film, tum_filmler):
    film_vektor = film_vektoru_olustur(model, tum_filmler[selected_film])
    film_vektorleri = {film: film_vektoru_olustur(model, tum_filmler[film]) for film in tum_filmler}
    skorlar = {film: cosine_similarity([film_vektor], [vektor])[0][0] for film, vektor in film_vektorleri.items()}
    return sorted(skorlar.items(), key=lambda x: x[1], reverse=True)[:5]  

# 📌 **Kodun Çalıştırılması**
script_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\scripts"
model_path = "word2vec_film_model.model"

# **Model varsa yükle, yoksa eğit ve kaydet**
if os.path.exists(model_path):
    film_model = Word2Vec.load(model_path)
    print("Mevcut model yüklendi!")
    tum_filmler = load_scripts(script_folder)  # Veri setini yine yükle
else:
    film_model, tum_filmler = train_word2vec(script_folder)
    print("Yeni model oluşturuldu ve kaydedildi!")

# Kullanıcıdan film ismi al
selected_film = input("Benzerlerini görmek istediğin filmi gir: ")

if selected_film not in tum_filmler:
    print(f"'{selected_film}' filmi bulunamadı! Lütfen mevcut senaryo dosyalarından birini seç.")
else:
    benzer_filmler = benzer_filmleri_bul(film_model, selected_film, tum_filmler)
    print(f"'{selected_film}' filmine en benzer 5 film:")
    for film, skor in benzer_filmler:
        print(f"{film}: Benzerlik skoru {skor:.4f}")
