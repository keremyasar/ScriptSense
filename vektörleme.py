import os
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

# Gerekli NLTK verilerini indir
nltk.download('punkt')

# Klasör yolları
stemmed_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\stemmed_dialogues"
lemmatized_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\lemmatized_dialogues"
tfidf_output_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\tfidf_results"

# Eğer tfidf sonuç klasörü yoksa oluştur
if not os.path.exists(tfidf_output_folder):
    os.makedirs(tfidf_output_folder)

def generate_tfidf(input_folder, output_filename):
    """CSV içeriğine göre gerçek ilerleme yüzdesini hesaplayan TF-IDF vektörleştirme."""
    texts = []
    filenames = []
    
    # 🔹 SADECE .txt dosyaları sayılıyor
    all_files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
    
    if not all_files:
        print(f"🚨 Hata: {input_folder} klasöründe hiç .txt dosyası yok!")
        return

    # 🔹 CSV dosyası oluşturulmadan önce satır sayısını takip etmek için
    total_sentences = 0  

    for file_name in all_files:
        file_path = os.path.join(input_folder, file_name)
        with open(file_path, "r", encoding="utf-8-sig") as f:
            content = f.read()
            sentences = sent_tokenize(content)  # Metni cümlelere ayır
            total_sentences += len(sentences)  # 🔹 Toplam cümle sayısını takip et
                
            for sentence in sentences:
                texts.append(sentence)
                filenames.append(f"{file_name} - {sentence[:30]}")  # Dosya adı + cümle başlığı

    # 🔹 TF-IDF hesaplanıyor
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()

    df = pd.DataFrame(tfidf_matrix.toarray(), index=filenames, columns=feature_names)
    output_file = os.path.join(tfidf_output_folder, output_filename)

    # 🔹 CSV'ye yazma işlemi
    df.to_csv(output_file)
    
    # 🔹 İlerleme yüzdesi hesapla
    processed_sentences = len(df)
    progress = (processed_sentences / total_sentences) * 100
    print(f"✅ TF-IDF başarıyla kaydedildi: {output_file} (%{progress:.2f})")

# Stemmed ve Lemmatized veriler için ayrı ayrı TF-IDF hesapla
print("\n🔹 TF-IDF Hesaplanıyor: Stemmed Veriler")
generate_tfidf(stemmed_folder, "tfidf_stemmed.csv")

print("\n🔹 TF-IDF Hesaplanıyor: Lemmatized Veriler")
generate_tfidf(lemmatized_folder, "tfidf_lemmatized.csv")

print("\n✅ Tüm TF-IDF işlemleri tamamlandı!")
