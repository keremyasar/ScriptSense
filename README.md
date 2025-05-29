# ScriptSense

veri seti indirme.py kodu çalıştırılıp imsdb.com sitesinden film senaryoları indirilmeli

diyalog ayıklama.py kodu çalıştırılıp senaryolardan diyaloglar ayıklanılmalı

stem ve lemma.py kodu ile diyaloglar köklerine indirilmiş hale getirilmeli

vektörleme.py kodu ile diyalogların stemmed ve lemmatized hallerinin TF-IDF vektörlemesi yapılıp tablo halinde görüntülenebilir

modelleme.py kodu ile stemmed ve lemmatized veri setleri için 8'şer toplamda da 16 model eğitimi yapılmalı

benzer kelime bulma modeli.py ile istenilirse kelimelerin Word2Vec Vektörleştirme sonuçlarına göre en yakın 5 kelimesi bulunabilir
      (bu kod çalıştırılırken stemmed bir model seçilirse girilen kelime stemmed edilmiş hali ile aranmalı
      lemmatized bir model seçilirse girilen kelime lemmatized edilmiş hali ile aranmalı)

son olarak benzer film bulma modeli.py kodu çalıştırılarak senaryo benzerliklerine göre film öneren model kullanıma hazır hale getirilmeli

Cümle_ayıklama.py kodu çalıştırılıp her metinden bir cümle seçilip output.csv dosyasına kaydettirme işlemi yapılmalı

Benzerlik_hesaplama.py kod dosyası ile output.csv dosyasını kullanılarak verilen örnek bir cümlenin 16 modele göre en benzer 5 cümlesi benzerlik_sonuclari.csv dosyasına yazdırılmalı

Jaccard.py ile benzerlik_sonuclari.csv dosyasına göre modellerin birbiri ile kıyasları yapılıp matris şeklinde jaccard_matrix.csv dosyasına kaydedilmeli

GEREKLİ KÜTÜPHANELER ve KURULUMLAR
import requests
from bs4 import BeautifulSoup
import os
import time
import re
import nltk
from urllib.parse import urljoin
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from textblob import Word
import pandas as pd
import numpy as np
import csv
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import gensim
from gensim.models import Word2Vec
from itertools import combinations


pip install requests beautifulsoup4 nltk textblob pandas scikit-learn gensim
pip install numpy scipy(gensim için gerekli)

