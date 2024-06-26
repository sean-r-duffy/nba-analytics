from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time

#Change to your username and password
username = ""
password = ""

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

    for i in range(0, max_n_rows_needed , 200):
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
                filename = 'output.csv'
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
        print(i)

    print(f'Data appended to {filename}')
finally:
    driver.quit()