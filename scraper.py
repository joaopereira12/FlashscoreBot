from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import warnings
from collections import defaultdict

warnings.filterwarnings("ignore")

chrome_options = Options()
chrome_options.add_argument("--headless")

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=chrome_options)
#driver.maximize_window()

url = "https://www.flashscore.pt/futebol/portugal/liga-portugal-betclic/resultados/"
driver.get(url)

try:
    WebDriverWait(driver, 8).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"))
    )
    button_cookies = driver.find_element(By.CSS_SELECTOR, "button#onetrust-accept-btn-handler")
    button_cookies.click()
except:
    print("✅ Cookies already closed or not needed.")

sleep(4)

round_elements = driver.find_elements(By.CSS_SELECTOR, "div.event__round--static")

if not round_elements:
    print("No rounds found. The page structure may have changed.")
    driver.quit()
    exit()

round_matches = defaultdict(list)

all_elements = driver.find_elements(By.CSS_SELECTOR, "div")

current_round = None 


for element in all_elements:
    class_name = element.get_attribute("class")

    if "event__round--static" in class_name:
        current_round = element.text.strip()

    elif "event__match" in class_name and current_round:
        try:
            event_time = element.find_element(By.CSS_SELECTOR, "div.event__time").text
            home_team = element.find_element(By.CSS_SELECTOR, "div.event__homeParticipant [data-testid='wcl-scores-simpleText-01']").text
            away_team = element.find_element(By.CSS_SELECTOR, "div.event__awayParticipant [data-testid='wcl-scores-simpleText-01']").text
            home_score = element.find_element(By.CSS_SELECTOR, "div.event__score--home").text
            away_score = element.find_element(By.CSS_SELECTOR, "div.event__score--away").text

            round_matches[current_round].append((event_time, home_team, away_team, home_score, away_score))
        except Exception as e:
            print(f"⚠️ Error extracting match details: {e}")

driver.quit()

for round_name, matches in round_matches.items():
    print(f"\n{round_name}")
    for match in matches:
        print(f"Match date: {match[0]} | {match[1]} {match[3]}-{match[4]} {match[2]}")
