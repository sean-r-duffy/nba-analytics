import os
import csv
import time
import pandas as pd
from typing import Union
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Environment variables must be loaded so that KaggleApi can be properly initiated (KAGGLE_USERNAME & KAGGLE_KEY)
load_dotenv()
from kaggle.api.kaggle_api_extended import KaggleApi


# TODO: Eliminate reused scraping code
def scrape_stathead_knn_stats(output_dir: str,
                              query_url: str,
                              n_players: int,
                              file_name: str) -> None:
    """
    Collect player data from stathead.com to CSV file

    :param output_dir: Directory in which to save CSV
    :param query_url: Stathead address from which to scrape data
    :param n_players: Number of player data rows to scrape
    :param file_name: Name of CSV file to save data to
    :rtype: None
    """
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


def scrape_stathead_teams(output_dir: object,
                          filename: str = 'team_stats.csv') -> None:
    """
    Collect team data from stathead.com to CSV file

    :param output_dir: Directory in which to save CSV
    :param filename: Name of CSV file to save data to
    :rtype: None
    """
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
                    filename = f'{output_dir}/{filename}'
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


def download_kaggle_set(kaggle_path: str,
                        output_dir: object,
                        filename: str) -> None:
    """
    Download full datasets from kaggle

    :param kaggle_path:
    :param output_dir: Directory in which to save CSV
    :param filename: Name of directory to save data to
    :rtype: None
    """
    kaggle_api = KaggleApi()
    kaggle_api.authenticate()

    kaggle_api.dataset_download_files(kaggle_path, path=f'{output_dir}/{filename}', unzip=True)


def get_df(df: Union[pd.DataFrame, str]) -> pd.DataFrame:
    """
    Returns df if type is DataFrame, else reads CSV to DataFrame

    :param df: Either a pandas DataFrame object or path to a CSV
    :rtype: DataFrame
    """
    if isinstance(df, pd.DataFrame):
        df = df.copy()
    else:
        df = pd.read_csv(df)

    return df


if __name__ == '__main__':
    # Directory in which to save output
    directory = 'data/external'

    # Team data From Stathead
    scrape_stathead_teams(directory)

    # Player datasets from Kaggle
    download_kaggle_set('wyattowalsh/basketball', directory, 'kaggle1')
    download_kaggle_set('sumitrodatta/nba-aba-baa-stats', directory, 'kaggle2')

    # Stathead addresses to scrape
    player_query = "https://stathead.com/basketball/player-season-finder.cgi?request=1&year_min=2001&year_max=2024&display_type=per_g&ccomp%5B2%5D=gt&cval%5B2%5D=8&cstat%5B2%5D=mp_per_g"
    all_star_query = "https://stathead.com/basketball/player-season-finder.cgi?request=1&year_min=2001&year_max=2024&display_type=per_g&as_selections_type=Y"
    college_query = "https://stathead.com/basketball/cbb/player-season-finder.cgi?request=1&order_by=pts_per_g&year_min=2001&year_max=2024&comp_id=NCAAM&team_success=ncaa_made&draft_status=drafted&draft_pick_type=overall"

    # Scraping player data from Stathead
    scrape_stathead_knn_stats(directory, player_query, 10000, "all_player_stats_00-24.csv")
    scrape_stathead_knn_stats(directory, all_star_query, 600, "allstar_stats_00-24.csv")
    scrape_stathead_knn_stats(directory, college_query, 1600, "college_player_stats_00-24.csv")
