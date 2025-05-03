import os
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from textblob import Word

# Gerekli NLTK verilerini indir
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Klasör yollarını belirle
dialogues_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\dialogues"
stemmed_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\stemmed_dialogues"
lemmatized_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\lemmatized_dialogues"

# Eğer klasörler yoksa oluştur
for folder in [stemmed_folder, lemmatized_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Stopwords listesi (İngilizce)
stop_words = set(stopwords.words("english"))

# Stemming ve Lemmatization nesneleri
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    """Verilen metne ön işleme uygula."""
    
    text = re.sub(r'<.*?>', '', text)  # HTML etiketlerini kaldır
    text = re.sub(r'[^a-zA-Zğüşıöç ]+', '', text)  # Özel karakterleri kaldır
    text = text.lower()  # Küçük harfe çevir

    tokens = word_tokenize(text)  # Tokenization (kelimeleri ayır)
    tokens = [word for word in tokens if word not in stop_words]  # Stop word removal

    # Lemmatization (TextBlob ile)
    lemmatized_tokens = [Word(word).lemmatize() for word in tokens]

    # Stemming (NLTK ile)
    stemmed_tokens = [stemmer.stem(word) for word in lemmatized_tokens]

    return " ".join(stemmed_tokens), " ".join(lemmatized_tokens)

# Tüm metin dosyalarını işle
for filename in os.listdir(dialogues_folder):
    if filename.endswith(".txt"):  # Sadece .txt dosyalarını işle
        input_file = os.path.join(dialogues_folder, filename)
        stemmed_output_file = os.path.join(stemmed_folder, f"{filename.replace('.txt', '_stemmed.txt')}")
        lemmatized_output_file = os.path.join(lemmatized_folder, f"{filename.replace('.txt', '_lemmatized.txt')}")

        # Dosyayı oku
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()

        # Ön işlemleri uygula
        stemmed_text, lemmatized_text = preprocess_text(text)

        # Stem işlemi dosyaya yaz
        with open(stemmed_output_file, "w", encoding="utf-8") as f:
            f.write(stemmed_text)

        # Lemmatization işlemi dosyaya yaz
        with open(lemmatized_output_file, "w", encoding="utf-8") as f:
            f.write(lemmatized_text)

        print(f"İşlenen dosyalar: {stemmed_output_file} ve {lemmatized_output_file}")
