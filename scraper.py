import time
from bs4 import BeautifulSoup
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

def init_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    return chrome_options

def init_driver(chrome_options):
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=chrome_options)
    return driver

def close_cookies(driver):
    try:
        WebDriverWait(driver, 8).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"))
        )
        button_cookies = driver.find_element(By.CSS_SELECTOR, "button#onetrust-accept-btn-handler")
        button_cookies.click()
    except:
        print("Cookies already closed or not needed.")

def create_soup(url):
    chrome_options = init_chrome()
    driver = init_driver(chrome_options)
    driver.get(url)
    time.sleep(4)  # Allow time for dynamic content to load

    html = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(html, "html.parser")
    return soup
def last_results_league(country, league):
    chrome_options = init_chrome()
    driver = init_driver(chrome_options)
    url = f"https://www.flashscore.pt/futebol/{country}/{league}/resultados/"
    driver.get(url)
    
    # Handle cookies popup if present
    close_cookies(driver)
    
    # Allow time for dynamic content to load
    time.sleep(4)
    
    # Get the fully rendered HTML from Selenium
    html = driver.page_source
    driver.quit()
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    round_matches = defaultdict(list)
    current_round = None

    # Iterate over all divs to maintain the page order
    for div in soup.find_all("div"):
        classes = div.get("class", [])
        if "event__round--static" in classes:
            current_round = div.get_text(strip=True)
        elif "event__match" in classes and current_round:
            try:
                event_time_elem = div.find("div", class_="event__time")
                event_time = event_time_elem.get_text(strip=True) if event_time_elem else ""
                
                home_team_elem = div.find("div", class_="event__homeParticipant")
                home_team = ""
                if home_team_elem:
                    home_team_span = home_team_elem.select_one("[data-testid='wcl-scores-simpleText-01']")
                    home_team = home_team_span.get_text(strip=True) if home_team_span else ""
                
                away_team_elem = div.find("div", class_="event__awayParticipant")
                away_team = ""
                if away_team_elem:
                    away_team_span = away_team_elem.select_one("[data-testid='wcl-scores-simpleText-01']")
                    away_team = away_team_span.get_text(strip=True) if away_team_span else ""
                
                home_score_elem = div.find("div", class_="event__score--home")
                home_score = home_score_elem.get_text(strip=True) if home_score_elem else ""
                
                away_score_elem = div.find("div", class_="event__score--away")
                away_score = away_score_elem.get_text(strip=True) if away_score_elem else ""
                
                round_matches[current_round].append((event_time, home_team, away_team, home_score, away_score))
            except Exception as e:
                print(f"Error extracting match details: {e}")
    return round_matches

def league_standings(country, league):
    url = f"https://www.flashscore.pt/futebol/{country}/{league}/classificacoes/"
    chrome_options = init_chrome()
    driver = init_driver(chrome_options)
    driver.get(url)
    close_cookies(driver)
    time.sleep(4)
    html = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(html, "html.parser")

    standings = []

    for div in soup.find_all("div", class_="ui-table__row"):
        team_name = div.find("a", class_="tableCellParticipant__name").get_text(strip=True)
        all_data = div.find_all("span", class_="table__cell--value")
        team_games = all_data[0].get_text(strip=True)
        team_wins = all_data[1].get_text(strip=True)
        team_draws = all_data[2].get_text(strip=True)
        team_losses = all_data[3].get_text(strip=True)
        team_score = all_data[4].get_text(strip=True)
        team_diff = all_data[5].get_text(strip=True)
        team_points = all_data[6].get_text(strip=True)
        standings.append((team_name, team_games, team_wins, team_draws, team_losses, team_score, team_diff, team_points))
    return standings

def league_next_fixtures(country, league):
    url = f"https://www.flashscore.pt/futebol/{country}/{league}/lista/"
    soup = create_soup(url)
    round_matches = defaultdict(list)
    current_round = None

    # Iterate over all divs to maintain the page order
    for div in soup.find_all("div"):
        classes = div.get("class", [])
        if "event__round--static" in classes:
            current_round = div.get_text(strip=True)
        elif "event__match" in classes and current_round:
            try:
                event_time_elem = div.find("div", class_="event__time")
                event_time = event_time_elem.get_text(strip=True) if event_time_elem else ""
                
                home_team_elem = div.find("div", class_="event__homeParticipant")
                home_team = ""
                if home_team_elem:
                    home_team_span = home_team_elem.select_one("[data-testid='wcl-scores-simpleText-01']")
                    home_team = home_team_span.get_text(strip=True) if home_team_span else ""
                
                away_team_elem = div.find("div", class_="event__awayParticipant")
                away_team = ""
                if away_team_elem:
                    away_team_span = away_team_elem.select_one("[data-testid='wcl-scores-simpleText-01']")
                    away_team = away_team_span.get_text(strip=True) if away_team_span else ""
                
                round_matches[current_round].append((event_time, home_team, away_team))
            except Exception as e:
                print(f"Error extracting match details: {e}")
    return round_matches

    

def get_team_page_url(country, league, team):
    url = f"https://www.flashscore.pt/futebol/{country}/{league}/classificacoes/"
    chrome_options = init_chrome()
    driver = init_driver(chrome_options)
    driver.get(url)
    time.sleep(4)  # Allow time for dynamic content to load

    html = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(html, "html.parser")
    team_url = None

    for a in soup.find_all("a", href=True):
        if "/equipa/" in a["href"]:
            text = a.get_text(strip=True)
            # Check if the team name is in the link text.
            if team.lower() in text.lower():
                team_url = "https://www.flashscore.pt" + a["href"]
                break
    return team_url

def team_info(country, league, team):
    team_info = defaultdict(list)
    url = get_team_page_url(country, league, team) + "resultados/"
    print(url)
    team_info["prev_matches"] = team_prev_matches(url)
    url = get_team_page_url(country, league, team) + "lista/"
    team_info["next_matches"] = team_next_matches(url)
    url = get_team_page_url(country, league, team) + "classificacoes/"
    team_info["standings"] = team_standings_championship(url)
    return team_info

# Returns the next 5 games of the team
def team_next_matches(url):
    soup = create_soup(url)
    results = []
    matches = soup.find_all("div", class_="event__match")
    
    
    for i in range(5):
        match_date = matches[i].find("div", class_="event__time").get_text()    
        home_team = matches[i].find("div", class_="event__homeParticipant").select_one("[data-testid='wcl-scores-simpleText-01']").get_text(strip=True)
        away_team = matches[i].find("div", class_="event__awayParticipant").select_one("[data-testid='wcl-scores-simpleText-01']").get_text(strip=True)     
        results.append((match_date, home_team, away_team))
    return results     

# returns the prev 5 games
def team_prev_matches(url):
    soup = create_soup(url)
    results = []
    matches = soup.find_all("div", class_="event__match")
    print(matches)
    
    for i in range(5):
        match_date = matches[i].find("div", class_="event__time").get_text()    
        home_team = matches[i].find("div", class_="event__homeParticipant").select_one("[data-testid='wcl-scores-simpleText-01']").get_text(strip=True)
        away_team = matches[i].find("div", class_="event__awayParticipant").select_one("[data-testid='wcl-scores-simpleText-01']").get_text(strip=True)     
        home_score = matches[i].find("div", class_="event__score--home").get_text(strip=True)
        away_score = matches[i].find("div", class_="event__score--away").get_text(strip=True)
        results.append((match_date, home_team, away_team, home_score, away_score))
    return results       

# returns the team standing in championship
def team_standings_championship(url):
    soup = create_soup(url)
    standings = []

    for div in soup.find_all("div", class_="ui-table__row"):
        team_name = div.find("a", class_="tableCellParticipant__name").get_text(strip=True)
        all_data = div.find_all("span", class_="table__cell--value")
        team_games = all_data[0].get_text(strip=True)
        team_wins = all_data[1].get_text(strip=True)
        team_draws = all_data[2].get_text(strip=True)
        team_losses = all_data[3].get_text(strip=True)
        team_score = all_data[4].get_text(strip=True)
        team_diff = all_data[5].get_text(strip=True)
        team_points = all_data[6].get_text(strip=True)
        standings.append((team_name, team_games, team_wins, team_draws, team_losses, team_score, team_diff, team_points))
    return standings



if __name__ == "__main__":
    round_matches = league_next_fixtures("portugal", "liga-portugal-betclic")
    
    for round_name, matches in round_matches.items():
        print(f"\n{round_name}")
        for match in matches:
            print(f"Match date: {match[0]} | {match[1]} vs {match[2]}")

    # standings = league_standings("inglaterra", "premier-league")
    # place = 1
    # for team in standings:
    #     print(f"{place}. {team[0]} | {team[7]}")
    #     place += 1
    # print(team_info("portugal","liga-portugal-betclic", "benfica" ))
