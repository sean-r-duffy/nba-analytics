import os
import csv
import time
import pandas as pd
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo, cumestatsplayer, playergamelog
from nba_api.stats.endpoints import draftcombinestats, draftcombinedrillresults, draftcombineplayeranthro, draftcombinespotshooting, draftcombinenonstationaryshooting, drafthistory
from nba_api.stats.static import players


def scrape_stathead_players():
    # Load login information
    load_dotenv()
    username = os.getenv('STATHEAD_USERNAME')
    password = os.getenv('STATHEAD_PASSWORD')

    driver = webdriver.Chrome()

    try:
        login_url = "https://stathead.com/users/login.cgi"
        driver.get(login_url)
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")

        username_field.send_keys(username)
        password_field.send_keys(password)

        login_button = driver.find_element(By.ID, "sh-login-button")
        login_button.click()
        time.sleep(5)

        # Change to how many rows needed to scrape
        max_n_rows_needed = 16000

        for i in range(0, max_n_rows_needed, 200):
            # Adapt URL for each Stathead Query
            url = f"https://stathead.com/basketball/player-season-finder.cgi?request=1&year_min=1980&display_type=advanced&ccomp%5B1%5D=gt&cval%5B1%5D=10&cstat%5B1%5D=mp_per_g&offset={i}"
            success = False
            while not success:
                try:
                    driver.get(url)
                    time.sleep(5)
                    element_to_hover = driver.find_element(By.XPATH, "//span[text()='Export Data']")
                    actions = ActionChains(driver)
                    actions.move_to_element(element_to_hover).perform()
                    switch_csv_button = driver.find_element(By.XPATH, "//button[text()='Get table as CSV (for Excel)']")
                    switch_csv_button.click()
                    time.sleep(0.5)
                    csv_data = driver.find_element(By.ID, 'csv_stats').text
                    lines = csv_data.split('\n')
                    rows = [line.split(',') for line in lines]
                    # Optional, change as needed
                    filename = '../../data/external/NBA_player_stats_1979-2024.csv'
                    if i == 0:
                        rows = rows[4:]
                    else:
                        rows = rows[5:]

                    with open(filename, 'a', newline='') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerows(rows)
                    success = True
                except:
                    time.sleep(5)
                    continue
            print(f'{i} rows added')

        print(f'Data appended to {filename}')
    finally:
        driver.quit()


def scrape_stathead_teams():
    # Load login information
    load_dotenv()
    username = os.getenv('STATHEAD_USERNAME')
    password = os.getenv('STATHEAD_PASSWORD')

    driver = webdriver.Chrome()

    try:
        login_url = "https://stathead.com/users/login.cgi"
        driver.get(login_url)
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")

        username_field.send_keys(username)
        password_field.send_keys(password)

        login_button = driver.find_element(By.ID, "sh-login-button")
        login_button.click()
        time.sleep(5)

        # Change to how many rows needed to scrape
        max_n_rows_needed = 1200

        for i in range(0, max_n_rows_needed, 200):
            # Adapt URL for each Stathead Query
            url = f"https://stathead.com/basketball/team-season-finder.cgi?request=1&year_min=1980&offset={i}"
            success = False
            while not success:
                try:
                    driver.get(url)
                    time.sleep(5)
                    element_to_hover = driver.find_element(By.XPATH, "//span[text()='Export Data']")
                    actions = ActionChains(driver)
                    actions.move_to_element(element_to_hover).perform()
                    switch_csv_button = driver.find_element(By.XPATH, "//button[text()='Get table as CSV (for Excel)']")
                    switch_csv_button.click()
                    time.sleep(0.5)
                    csv_data = driver.find_element(By.ID, 'csv_stats').text
                    lines = csv_data.split('\n')
                    rows = [line.split(',') for line in lines]
                    # Optional, change as needed
                    filename = '../../data/external/NBA_team_stats_1979-2024.csv'
                    if i == 0:
                        rows = rows[4:]
                    else:
                        rows = rows[5:]

                    with open(filename, 'a', newline='') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerows(rows)
                    success = True
                except:
                    time.sleep(5)
                    continue
            print(f'{i} rows added')

        print(f'Data appended to {filename}')
    finally:
        driver.quit()


def scrape_combine():
    years = ['2000-01', '2001-02', '2002-03', '2003-04', '2004-05', '2005-06',
             '2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12',
             '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18',
             '2018-19', '2019-20', '2020-21', '2021-22', '2022-23', '2023-24', '2024-25']

    driver = webdriver.Chrome()
    # table_cols = ['player', 'pos', 'bodyfat%', 'hand_len_in', 'hand_width_in', 'height_wo_shoes', 'height_w_shoes', 'standing_reach', 'weight_lbs', 'wingspan', 'year']
    table_cols = ['player', 'pos', 'lane_agility_s', 'shuttle_run_s', 'three_q_sprint_s', 'standing_vert_in',
                  'max_vert_in', 'max_bench_reps', 'year']
    df = pd.DataFrame(columns=table_cols)

    for year in years:
        # url = f'https://www.nba.com/stats/draft/combine-anthro?SeasonYear={year}'
        url = f'https://www.nba.com/stats/draft/combine-strength-agility?SeasonYear={year}'
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "tr")))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            rows = soup.find('tbody').find_all('tr')
            for row in rows:
                row_data = []
                cells = row.find_all('td')
                for cell in cells:
                    row_data.append(cell.get_text(strip=True))
                row_data.append(year)
                if len(row_data) == len(table_cols):  # Ensure row data matches column count
                    df.loc[len(df)] = row_data
                else:
                    print(f"Skipping row due to mismatch in column count: {row_data}")
        except Exception as e:
            print(f"Error with year {year}\n{e}")
        time.sleep(1)

    driver.quit()
    df.to_csv('../../data/external/NBA_combine_stats_2000-2024.csv', index=False)


def nba_api_players():
    all_players = pd.json_normalize(players.get_players())
    career_stats_df = pd.DataFrame()
    for player_id in all_players['id'].to_list():
        career_stats_df = pd.concat([career_stats_df,
                                     playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]])


if __name__ == '__main__':
    scrape_stathead_players()
    scrape_stathead_teams()
    scrape_combine()
