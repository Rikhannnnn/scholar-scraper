from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time, random, re, json, sys
from datetime import datetime
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances
from sklearn.metrics import jaccard_score
from sklearn.preprocessing import Binarizer
from os import link
import requests as rq
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from deep_translator import GoogleTranslator

#region Dapat data dari inputan user
namaPenulis = sys.argv[1]
jumlahData = int(sys.argv[2])
keyword = sys.argv[3] 
keywords = keyword.split("+") #Modeling+optimization+ --> ["modeling", "optimization"]  
keywords = list(filter(None, keywords)) 
keywords = ' '.join(keywords) #Modeling optimization
#endregion

#region Seting driver
options = webdriver.ChromeOptions() # chrome
# options.add_argument("--headless=new")
options.add_argument("--start-maximized") #Full Display
options.add_argument("--disable-blink-features=AutomationControlled") # Menyembunyikan bahwa browser dikendalikan secara automation
options.add_argument("--disable-infobars") # Mengurangi kemungkinan deteksi otomatis
options.add_argument("--disable-extensions") 

options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 15) # maksimal 15 detik sampai elemen muncul
#endregion

#region Searching penulis
search_url = "https://scholar.google.com/scholar?q=" + namaPenulis 
driver.get(search_url)
time.sleep(random.uniform(3, 5))
#endregion


#region Translate keyword
newKeyword = GoogleTranslator(source="auto", target="id").translate(keywords) #Modeling optimization --> pemodelan optimasi
#endregion


#region Stem/Stop keyword
stemmer = StemmerFactory().create_stemmer() #mengubah ke kata dasar
stopper = StopWordRemoverFactory().create_stop_word_remover() # contoh: di, ke, yang, dan, untuk

stem_keyword = stemmer.stem(newKeyword) #pemodelan optimasi --> model optimasi
stop_keyword = stopper.remove(stem_keyword) 
#endregion


#region Open Profil Author
profile_link = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "h4.gs_rt2 a"))
)

profile_url = profile_link.get_attribute("href")

driver.get(profile_url)
#endregion


#region Get List Jurnal
articles = driver.find_elements(By.CSS_SELECTOR, "a.gsc_a_at")

top_data = []
sample_data = []

for article in articles[:jumlahData]:
    title = article.text
    link = article.get_attribute("href")

    #region Translate Judul
    newJudul = GoogleTranslator(source="auto", target="id").translate(title)
    #endregion


    #region Stem/Stop judul
    stem_judul = stemmer.stem(newJudul)
    stop_judul = stopper.remove(stem_judul)
    #endregion


    #region Tf/Idf
    sample_data.append(stop_judul)
    #endregion


    top_data.append({
        "judul": title,
        "similarity": 0,
        "link": link
    })
#endregion

#region TF-IDF
sample_data.append(stop_keyword)

tfidf = TfidfVectorizer(norm = None, sublinear_tf = True)
vector_tfidf = tfidf.fit_transform(sample_data)
total = len(sample_data)
#endregion


#region Jaccard
binarizer = Binarizer()
vector_biner = binarizer.fit_transform(vector_tfidf.toarray())
for i in range(total-1):
    hasil = jaccard_score(vector_biner[total-1], vector_biner[i], average="binary")
    top_data[i]["similarity"] = hasil
#endregion


#region Get Detail Jurnal
article_data = []
for art in top_data:
    driver.get(art["link"])
    
    time.sleep(random.uniform(3, 5))

    try:
        linkJurnal = driver.find_element(By.CSS_SELECTOR, "a.gsc_oci_title_link").get_attribute("href")
    except:
        linkJurnal = art["link"] 
    detail = driver.find_elements(By.CSS_SELECTOR, "div.gs_scl")
    
    pengarang = ""
    tanggal_terbit = ""
    kutipan = 0
    jurnal = ""
    
    for row in detail:
        field = row.find_element(By.CSS_SELECTOR, ".gsc_oci_field").text.strip()
        value = row.find_element(By.CSS_SELECTOR, ".gsc_oci_value").text.strip()
        
        if field == "Pengarang" or field == "Authors":
            pengarang = value
        elif field == "Tanggal terbit" or field == "Publication date":
            try:
                tanggal_terbit = datetime.strptime(value, "%Y/%m/%d").strftime("%d/%m/%Y")
            except ValueError:
                tanggal_terbit = value
        elif field == "Total kutipan" or field == "Total citations":
            match = re.search(r"\d+", value)
            kutipan = int(match.group()) if match else 0
        elif field == "Jurnal" or field == "Journal":
            jurnal = value

    article_data.append({
        "judul": art["judul"],
        "link": linkJurnal,
        "pengarang": pengarang,
        "tanggal_terbit": tanggal_terbit,
        "total_kutipan": kutipan,
        "jurnal": jurnal,
        "similarity": art["similarity"]
    })

    time.sleep(random.uniform(1, 2))
#endregion

#region sorting and return
def get_similarity(item):
    return item["similarity"]

article_data.sort(
    key=get_similarity,
    reverse=True
)

print(json.dumps(article_data))
#endregion