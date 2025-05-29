import pandas as pd
import numpy as np
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
import re

# **Cümle çıkartma fonksiyonu**
def extract_meaningful_sentence(text):
    """ Metinden anlamlı bir cümle alır. """
    sentences = re.split(r'[.?!]', text)  # Noktalama işaretleriyle böl
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10 and " " in s]  # Kısa veya anlamsız cümleleri ele
    return sentences[0] if sentences else text  # İlk anlamlı cümleyi al, yoksa tüm metni döndür

# **Modeller ve dosya yolları**
tfidf_models = ["tfidf_lemmatized", "tfidf_stemmed"]
word2vec_models = [
    "word2vec_lemmatized_cbow_window2_dim100",
    "word2vec_lemmatized_skipgram_window2_dim100",
    "word2vec_lemmatized_cbow_window4_dim100",
    "word2vec_lemmatized_skipgram_window4_dim100",
    "word2vec_lemmatized_cbow_window2_dim300",
    "word2vec_lemmatized_skipgram_window2_dim300",
    "word2vec_lemmatized_cbow_window4_dim300",
    "word2vec_lemmatized_skipgram_window4_dim300",
    "word2vec_stemmed_cbow_window2_dim100",
    "word2vec_stemmed_skipgram_window2_dim100",
    "word2vec_stemmed_cbow_window4_dim100",
    "word2vec_stemmed_skipgram_window4_dim100",
    "word2vec_stemmed_cbow_window2_dim300",
    "word2vec_stemmed_skipgram_window2_dim300",
    "word2vec_stemmed_cbow_window4_dim300",
    "word2vec_stemmed_skipgram_window4_dim300"
]

# **Veri setini yükleme**
csv_file = "F:\\DOĞAL DİL\\output.csv"
df = pd.read_csv(csv_file)
word2vec_folder = "F:\\DOĞAL DİL\\word2vec_models"

# **Giriş metni**
query_text = "As the protagonist hesitates at the crossroads, the camera lingers, capturing the weight of the decision hanging in the air."

# **Sonuçları saklamak için boş liste**
results = []

# **TF-IDF Benzerlik Hesaplamaları**
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["content"])
query_vec = vectorizer.transform([query_text])

for model_name in tfidf_models:
    cosine_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = cosine_scores.argsort()[-5:][::-1]
    
    for idx in top_indices:
        best_sentence = extract_meaningful_sentence(df.iloc[idx]['content'])  # ❗ Yalnızca en benzer cümleyi al
        results.append([model_name, df.iloc[idx]['document_id'], cosine_scores[idx], best_sentence])

# **Word2Vec Benzerlik Hesaplamaları**
def get_sentence_vector(sentence, model):
    """ Kelimelerin ortalama vektörünü hesaplar. """
    vectors = [model.wv[word] for word in sentence.split() if word in model.wv]
    return np.mean(vectors, axis=0) if vectors else None

for model_name in word2vec_models:
    model_path = f"{word2vec_folder}\\{model_name}.model"

    try:
        model = Word2Vec.load(model_path)
    except FileNotFoundError:
        print(f"Hata: Model dosyası bulunamadı -> {model_path}")
        continue

    query_vector = get_sentence_vector(query_text, model)

    if query_vector is not None:
        doc_vectors = []
        valid_indices = []

        for idx, row in df.iterrows():
            vec = get_sentence_vector(row["content"], model)
            if vec is not None:
                doc_vectors.append(vec)
                valid_indices.append(idx)

        cosine_scores = cosine_similarity([query_vector], doc_vectors).flatten()

        if len(cosine_scores) == 0:
            print(f"Hata: {model_name} modeli için cosine similarity hesaplanamadı.")
            continue

        top_indices = np.array(valid_indices)[cosine_scores.argsort()[-5:][::-1]]
        top_indices = [idx for idx in top_indices if idx in valid_indices and idx < len(df)]

        for idx in top_indices:
            try:
                best_sentence = extract_meaningful_sentence(df.iloc[idx]['content'])
                results.append([model_name, df.iloc[idx]['document_id'], cosine_scores[idx], best_sentence])
            except IndexError:
                print(f"Hata: indeks {idx} veri çerçevesinde mevcut değil! Atlanıyor...")



# **Sonuçları CSV Dosyasına Kaydetme**
output_csv = "benzerlik_sonuclari.csv"

with open(output_csv, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Model Adı", "Document ID", "Benzerlik Skoru", "İçerik"])
    writer.writerows(results)

print(f"\n✅ Benzerlik sonuçları '{output_csv}' dosyasına kaydedildi!")
