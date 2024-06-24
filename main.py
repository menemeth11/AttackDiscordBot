from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import tajne
import requests

options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False) # zmniejsza ilosc logów generwoancyh
options.add_experimental_option("excludeSwitches", ["enable-logging"]) # zmniejsza ilosc generowanych logów
options.add_argument("--disable-blink-features=AutomationControlled") # wyłącza funkcje używane przez chrome informujace o tym, że to automat
options.add_argument("--disable-infobars") # pozybcie sie baneru, że przeglądarka jest automatyczna
options.add_argument("--disable-popup-blocking") # blokowanie popupów blokujących działanie
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36") #podawanie się za użytkowanika 
#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 #win10

#Docelowo chcemy lecieć na tym niżej. Wyłączenie w pełni UI. Najlepsza wydajność szybkośc itd ##Później dorobić "klienta" w TKinter
#options.add_argument("--headless")

options.add_argument("--start-maximized") # pełen ekran
options.add_experimental_option("detach", True) # przeglądarka nie zamyka sie na koniec kodu  

driver = webdriver.Chrome(options=options)

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#Totalna podstawa/ punkt wyjścia

driver.get("https://pl.grepolis.com/")

try:
    imput_login = driver.find_element(By.ID, "login_userid")
    imput_login.clear()
    imput_login.send_keys(tajne.login)
    time.sleep(2)
    imput_password = driver.find_element(By.ID, "login_password")
    imput_password.clear()
    imput_password.send_keys(tajne.password + Keys.ENTER)
    time.sleep(2)
    world = driver.find_element(By.XPATH, '//*[@id="worlds"]/div/ul/li[1]/div')
    world.click()
except:
    print("strona się nie załadowała / logowanie się nie powiodło")

time.sleep(5) 
close = driver.find_element(By.CLASS_NAME, "close_all") ### to 
close.click() 

time.sleep(1)

def send_discord_embed(webhook_url, title, description, color=0xFF00FF):
    embed = {
        "title": title,
        "description": description,
        "color": color
    }

    data = {
        "username": "Mazur v2",
        "embeds": [embed]
    }

    response = requests.post(webhook_url, json=data)
    
    if response.status_code == 204:
        print("Wiadomość została wysłana.")
    else:
        print(f"Błąd: {response.status_code}, {response.text}")


attack_overview = driver.find_element(By.ID, "toolbar_activity_attack_indicator")
attack_overview.click()
time.sleep(2)

ul_element = driver.find_element(By.XPATH, '//*[@id="tab_all"]//*[@id="command_overview"]')
time.sleep(2)
li_elements = ul_element.find_elements(By.XPATH, './li[starts-with(@id, "command_")]')

attacks = [] 

for attack in li_elements:
    attack_type = attack.get_attribute("data-command_type")
    if "attack_land" in attack_type:
        attacks.append(attack)
        text_box = attack.find_element(By.CLASS_NAME, 'cmd_info_box') #czy to jest ważne? 
        
        dane = attack.find_element(By.CLASS_NAME, 'cmd_span')
        dane = dane.text
        
        dane = dane.replace(")", "(")
        podzielone = dane.split("(") #.strip()

        stringSplit = attack.get_attribute("id")
        number = stringSplit.split('_')
        attack_arive = attack.find_element(By.CLASS_NAME, f'troops_arrive_at.eta-arrival-{number[1]}')

        ###Create discord message
        title = "Info o ataku!!"
        description = f"Atakowany gracz: **{podzielone[3].strip()}**\nAtakowane miasto: ** {podzielone[2].strip()} **\nAtakujące miasto: {podzielone[0]}\nAtakujący gracz: {podzielone[1].strip()}\n**Czas przybycia: {attack_arive.text}**\n@everyone "
        send_discord_embed(tajne.webhook_url, title, description)
        time.sleep(1)
        
    else:
        continue