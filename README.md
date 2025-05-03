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


GEREKLİ KÜTÜPHANELER ve KURULUMLAR
import requests
from bs4 import BeautifulSoup
import os
import time
import re
import nltk
from urllib.parse import urljoin
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from textblob import Word
import pandas as pd
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import gensim
from gensim.models import Word2Vec


pip install requests beautifulsoup4 nltk textblob pandas scikit-learn gensim
pip install numpy scipy(gensim için gerekli)

