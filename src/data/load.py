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
load_dotenv()
from kaggle.api.kaggle_api_extended import KaggleApi


def scrape_stathead_players(output_dir):
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
                    filename = f'{output_dir}/NBA_player_stats_1979-2024.csv'
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

def scrape_stathead_KNN_stats(output_dir, query_url, n_players, file_name):
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
        max_n_rows_needed = n_players

        for i in range(0, max_n_rows_needed, 200):
            # Adapt URL for each Stathead Query
            url = f"{query_url}&offset={i}"
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
                    filename = f'{output_dir}/{file_name}'
                    if i == 0:
                        rows = rows[5:]
                    else:
                        rows = rows[6:]

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

def scrape_stathead_teams(output_dir):
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
                    filename = f'{output_dir}/NBA_team_stats_1979-2024.csv'
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


def scrape_combine(output_dir):
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
    df.to_csv(f'{output_dir}/NBA_combine_stats_2000-2024.csv', index=False)


def download_kaggle_sets(output_dir):
    kaggle_api = KaggleApi()
    kaggle_api.authenticate()

    dataset_1 = 'wyattowalsh/basketball'
    dataset_2 = 'sumitrodatta/nba-aba-baa-stats'
    kaggle_api.dataset_download_files(dataset_1, path=f'{output_dir}/kaggle1', unzip=True)
    kaggle_api.dataset_download_files(dataset_2, path=f'{output_dir}/kaggle2', unzip=True)


if __name__ == '__main__':
    directory = 'data/external'
    scrape_stathead_players(directory)
    scrape_stathead_teams(directory)
    scrape_combine(directory)
    download_kaggle_sets(directory)
    
    directory = 'data/interim'
    player_query = "https://stathead.com/basketball/player-season-finder.cgi?request=1&year_min=2001&year_max=2024&display_type=per_g&ccomp%5B2%5D=gt&cval%5B2%5D=8&cstat%5B2%5D=mp_per_g"
    all_star_query = "https://stathead.com/basketball/player-season-finder.cgi?request=1&year_min=2001&year_max=2024&display_type=per_g&as_selections_type=Y"
    college_query = "https://stathead.com/basketball/cbb/player-season-finder.cgi?request=1&order_by=pts_per_g&year_min=2001&year_max=2024&comp_id=NCAAM&team_success=ncaa_made&draft_status=drafted&draft_pick_type=overall"
    scrape_stathead_KNN_stats(directory, player_query, 10000, "all_player_stats_00-24.csv")
    scrape_stathead_KNN_stats(directory, all_star_query, 600, "allstar_stats_00-24.csv")
    scrape_stathead_KNN_stats(directory, college_query, 1600, "college_player_stats_00-24.csv")
