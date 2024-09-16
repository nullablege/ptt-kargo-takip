from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse, parse_qs


options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-blink-features=AutomationControlled")


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

print("Lutfen secim yapiniz :\n1.Kargo Takip Kodu kullanarak detaya ulasma \n2.SMS İle yollanan baglanti ile detaya ulasma ( Data Detaylı )")
secim = input()
if secim == "1":
    
    url = "https://gonderitakip.ptt.gov.tr/"
    driver.get(url)
    search = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.ID, "search-area"))  
    )
    kargoTakip = input("Kargo takip kodunu giriniz :")
    search.send_keys(kargoTakip)
    search.send_keys(Keys.RETURN)
    img = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.CLASS_NAME,"img-fluid"))  
    )
    imgsrc = img.get_attribute('src')
    if imgsrc == "/Content/images/gonderitakiplogolar-5-.png":
        durum = "Kabul Edildi ,Transfer Sürecinde, İl İçi Aktarmada, Dağıtımda, Teslim Edildi"
    elif imgsrc == "/Content/images/gonderitakiplogolar-4-.png":
        durum = "Kabul Edildi ,Transfer Sürecinde, İl İçi Aktarmada, Dağıtımda"
    elif imgsrc == "/Content/images/gonderitakiplogolar-3-.png":
        durum = "Kabul Edildi ,Transfer Sürecinde, İl İçi Aktarmada"
    elif imgsrc == "/Content/images/gonderitakiplogolar-2-.png":
        durum = "Kabul Edildi ,Transfer Sürecinde"
    elif imgsrc == "/Content/images/gonderitakiplogolar-1-.png":
        durum = "Kabul Edildi"
    else:
        durum = "Durum kontrolunde hata oldu."
    cikisElement = driver.find_element(By.CSS_SELECTOR,"body > main > div > div:nth-child(4) > div:nth-child(1)")
    varisElement = driver.find_element(By.CSS_SELECTOR,"body > main > div > div:nth-child(4) > div:nth-child(2)")
    gonderici = cikisElement.find_elements(By.CLASS_NAME,"list-inline-item")
    gonderici_adi = gonderici[0].text
    gonderici_adres = gonderici[1].text
    gonderimTarihi = gonderici[2].text
    gonderici_il_ilce = driver.find_element(By.CSS_SELECTOR,"body > main > div > div:nth-child(4) > div:nth-child(1) > div > div > div > div.col-sm-8.col-md-8 > span").text
    alici = varisElement.find_elements(By.CLASS_NAME,"list-inline-item")
    alici_adi = alici[0].text
    alici_adres = alici[1].text
    alici_il_ilce = driver.find_element(By.CSS_SELECTOR,"body > main > div > div:nth-child(4) > div:nth-child(2) > div > div > div > div.col-sm-8.col-md-8 > span").text
    print(f"{gonderici_adi} - {alici_adi} \nGonderici Adres : {gonderici_adres} Alici Adres : {alici_adres}")
    print(f"{alici_il_ilce} - {gonderici_il_ilce}")
    print("Kargo Adımları : ")
    detayBtn = driver.find_element(By.ID,"activityButton")
    detayBtn.click()
    table = driver.find_element(By.CSS_SELECTOR,"#shipActivity > div > div > table")
    kol1 = driver.find_element(By.CSS_SELECTOR,"#shipActivity > div > div > table > thead > tr > th:nth-child(1)").text
    kol2 = driver.find_element(By.CSS_SELECTOR,"#shipActivity > div > div > table > thead > tr > th:nth-child(2)").text
    kol3 = driver.find_element(By.CSS_SELECTOR,"#shipActivity > div > div > table > thead > tr > th:nth-child(3)").text
    kol4 = driver.find_element(By.CSS_SELECTOR,"#shipActivity > div > div > table > thead > tr > th:nth-child(4)").text
    kol5 = driver.find_element(By.CSS_SELECTOR,"#shipActivity > div > div > table > thead > tr > th:nth-child(5)").text
    print(f"{kol1.center(20)} {kol2.center(20)} {kol3.center(20)} {kol4.center(20)} {kol5.center(20)}")
    tbody = driver.find_element(By.CSS_SELECTOR,"#shipActivity > div > div > table > tbody")
    trler = tbody.find_elements(By.TAG_NAME,"tr")
    for tr in trler:
        tdler = tr.find_elements(By.TAG_NAME,"td")
        print(f"{tdler[0].text.center(20)} {tdler[1].text.center(20)} {tdler[2].text.center(20)} {tdler[3].text.center(20)} {tdler[4].text.center(20)}")
elif secim == "2":
    #baglantı
    url = input("Url giriniz :")
    driver.get(url)
    main = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.ID, "main_inner"))  
    )
    #gonderici
    gonderici_ad = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:fieldSorguSonucBarkod5 > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > label").text
    gonderici_adres = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:fieldSorguSonucBarkod5 > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > label").text
    gonderici_ilce = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:fieldSorguSonucBarkod5 > div > table > tbody > tr:nth-child(3) > td:nth-child(2) > label").text
    gonderici_il = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:fieldSorguSonucBarkod5 > div > table > tbody > tr:nth-child(4) > td:nth-child(2) > label").text
    #alici
    alici_ad = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:fieldSorguSonucBarkod2 > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > label").text
    alici_adres = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:fieldSorguSonucBarkod2 > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > label").text
    alici_ilce = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:fieldSorguSonucBarkod2 > div > table > tbody > tr:nth-child(3) > td:nth-child(2) > label").text
    alici_il = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:fieldSorguSonucBarkod2 > div > table > tbody > tr:nth-child(4) > td:nth-child(2) > label").text
    #gonderi bilgileri
    gonderi_agirlik_desi = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:fieldSorguSonucBarkod4 > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > label").text
    gonderi_odeme = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:fieldSorguSonucBarkod4 > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > label").text
    gonderi_ucreti = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:fieldSorguSonucBarkod4 > div > table > tbody > tr:nth-child(3) > td:nth-child(4) > label").text
    gonderi_on_gorulen_tes_tar = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:fieldSorguSonucBarkod4 > div > table > tbody > tr:nth-child(4) > td:nth-child(2) > label").text
    gonderi_ek_hizmet = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:fieldSorguSonucBarkod4 > div > table > tbody > tr:nth-child(1) > td:nth-child(4) > label").text
    gonderi_referans = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:fieldSorguSonucBarkod4 > div > table > tbody > tr:nth-child(4) > td:nth-child(4) > label").text
    if not gonderi_on_gorulen_tes_tar:
        gonderi_on_gorulen_tes_tar = "Girilmemis"
    if not gonderi_referans:
        gonderi_referans = "Girilelmis"
    #teslim bilgileri 
    teslim_alan_yakinligi = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:fieldSorguSonucBarkod1 > div > table > tbody > tr > td:nth-child(2) > label").text
    teslim_tarihi = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:fieldSorguSonucBarkod1 > div > table > tbody > tr > td:nth-child(4) > label").text
    if not teslim_alan_yakinligi :
        teslim_alan_yakinligi = "Teslim Alinmamis"
        teslim_tarihi = "Teslim Alinmamis"
    gonderi_no = driver.current_url
    gonderi_no = urlparse(gonderi_no)
    gonderi_no = parse_qs(gonderi_no.query)
    gonderi_no = gonderi_no.get('barkod', [None])[0]
    print(f"{gonderi_no.center(30)} Nolu Gönderi :")
    print(f"{"gonderici".center(20)} - {"alici".center(20)}")
    print(f"Ad : {gonderici_ad.center(20)} - {alici_ad.center(20)} ")
    print(f"Adres : {gonderici_adres.center(12)} - {alici_adres.center(20)} ")
    print(f"İl / İlce : {gonderici_il.center(12)} / {gonderici_ilce.center(20)}")
    print(f"{"Gonderi Bilgileri".center(34)}")
    print(f"Agirlik / Desi : {gonderi_agirlik_desi.center(20)}")
    print(f"{gonderi_ucreti+" Ucreti "+gonderi_odeme} ")
    print(f"Tahmini teslimat tarihi {gonderi_on_gorulen_tes_tar}")
    print(f"Ek hizmet : {gonderi_ek_hizmet}")
    print(f"Gonderi Referans : {gonderi_referans}")
    #Gonderi hareketleri 
    tablo = driver.find_element(By.CSS_SELECTOR,"#j_idt7\:j_idt10\:talimat > div > table")
    print(f"{"Barkod No".center(20)} {"Gonderi Durum".center(20)} {"İl Adı".center(20)} {"Merkez Adı".center(20)} {"Şube Adı".center(20)} {"İşlem Tarihi".center(20)} {"İşlem Saati".center(20)}")
    trler = tablo.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "td")
    sayac = 0
    for td in trler:
        print(f"{td.text.center(21)}", end="")
        sayac+=1
        if sayac % 7 == 0:
            print("")

    if teslim_alan_yakinligi :
        print(f"{teslim_tarihi[0:4]}.{teslim_tarihi[4:6]}.{teslim_tarihi[6:8]} Tarihinde {teslim_alan_yakinligi} Tarafından Teslim Edilmistir. ")

else:
    pass