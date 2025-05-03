import os
import re
import gensim
from gensim.models import Word2Vec

# Klasör yolları
word2vec_output_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\word2vec_models"

# Eğer word2vec modeli klasörü yoksa oluştur
if not os.path.exists(word2vec_output_folder):
    os.makedirs(word2vec_output_folder)

parameters = [
    {'model_type': 'cbow', 'window': 2, 'vector_size': 100},
    {'model_type': 'skipgram', 'window': 2, 'vector_size': 100},
    {'model_type': 'cbow', 'window': 4, 'vector_size': 100},
    {'model_type': 'skipgram', 'window': 4, 'vector_size': 100},
    {'model_type': 'cbow', 'window': 2, 'vector_size': 300},
    {'model_type': 'skipgram', 'window': 2, 'vector_size': 300},
    {'model_type': 'cbow', 'window': 4, 'vector_size': 300},
    {'model_type': 'skipgram', 'window': 4, 'vector_size': 300}
]

def preprocess_text(text):
    """Metni temizle ve kelimeleri çıkar."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Zğüşıöç ]+', '', text)
    words = text.split()
    return words

def train_word2vec(input_folder, data_type):
    """Belirtilen veri seti ile tüm parametre kombinasyonları için Word2Vec modeli eğitir."""
    texts = []

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(input_folder, file_name)
            with open(file_path, "r", encoding="utf-8-sig") as f:
                texts.append(preprocess_text(f.read()))

    for param in parameters:
        model_type = param['model_type']
        window = param['window']
        vector_size = param['vector_size']
        sg = 1 if model_type == "skipgram" else 0

        model = Word2Vec(sentences=texts, vector_size=vector_size, window=window, sg=sg, workers=4)
        model_filename = f"word2vec_{data_type}_{model_type}_window{window}_dim{vector_size}.model"
        model.save(os.path.join(word2vec_output_folder, model_filename))
        print(f"Model başarıyla kaydedildi: {model_filename}")

stemmed_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\stemmed_dialogues"
lemmatized_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\lemmatized_dialogues"

# Stemmed ve Lemmatized veriler için ayrı ayrı model eğit
train_word2vec(stemmed_folder, "stemmed")
train_word2vec(lemmatized_folder, "lemmatized")
