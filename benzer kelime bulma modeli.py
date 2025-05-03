from gensim.models import Word2Vec

# Model dosyasını yükle
model_path = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\word2vec_models\\word2vec_stemmed_cbow_window2_dim100.model"
model = Word2Vec.load(model_path)

# Örnek kelime seçimi
kelime = "boy"  # Buraya analiz etmek istediğin kelimeyi yaz

# Kelimenin en yakın 5 komşusunu getir
benzer_kelimeler = model.wv.most_similar(kelime, topn=5)

print(f"'{kelime}' kelimesinin en yakın 5 kelimesi:")
for kelime, skor in benzer_kelimeler:
    print(f"{kelime}: {skor:.4f}")
