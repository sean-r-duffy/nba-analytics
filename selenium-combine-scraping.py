from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

years = ['2000-01', '2001-02', '2002-03', '2003-04', '2004-05', '2005-06',
         '2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12', 
         '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18',
         '2018-19', '2019-20', '2020-21', '2021-22', '2022-23', '2023-24', '2024-25']

driver = webdriver.Chrome()
# table_cols = ['player', 'pos', 'bodyfat%', 'hand_len_in', 'hand_width_in', 'height_wo_shoes', 'height_w_shoes', 'standing_reach', 'weight_lbs', 'wingspan', 'year']
table_cols = ['player', 'pos', 'lane_agility_s', 'shuttle_run_s', 'three_q_sprint_s', 'standing_vert_in', 'max_vert_in', 'max_bench_reps', 'year']
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
df.to_csv('NBA_combine_measurements_2.csv', index=False)
