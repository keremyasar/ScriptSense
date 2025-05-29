import pandas as pd
import numpy as np
from itertools import combinations

# **CSV dosyasını yükleme**
csv_file = "benzerlik_sonuclari.csv"
df = pd.read_csv(csv_file)

# **Her modelin ilk 5 sıralamasını al**
model_results = {}
for model_name in df["Model Adı"].unique():
    top_docs = set(df[df["Model Adı"] == model_name]["Document ID"][:5])  # İlk 5 sonucu al
    model_results[model_name] = top_docs

# **Jaccard benzerlik hesaplama fonksiyonu**
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

# **Jaccard matrisi oluşturma**
models = list(model_results.keys())
jaccard_matrix = pd.DataFrame(np.zeros((len(models), len(models))), index=models, columns=models)

# **Model çiftlerini karşılaştırarak Jaccard benzerliğini hesapla**
for model1, model2 in combinations(models, 2):
    jaccard_score = jaccard_similarity(model_results[model1], model_results[model2])
    jaccard_matrix.loc[model1, model2] = jaccard_score
    jaccard_matrix.loc[model2, model1] = jaccard_score

# **Köşegenleri 1.00 olarak ayarla (modelin kendisiyle kıyası)**
np.fill_diagonal(jaccard_matrix.values, 1.0)

# **Sonucu CSV dosyasına kaydet**
output_csv = "jaccard_matrix.csv"
jaccard_matrix.to_csv(output_csv)

print(f"\n✅ Jaccard benzerlik matrisi '{output_csv}' dosyasına kaydedildi!")
