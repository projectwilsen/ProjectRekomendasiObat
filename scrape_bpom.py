from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
chrome_options = Options()
options = [
    "--headless",
    f"--user-agent={user_agent}"
]
for option in options:
    chrome_options.add_argument(option)

url = "https://cekbpom.pom.go.id/obat"

try:
    # run in GitHub action
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=chrome_options)
    driver.get(url)
    print("driver based on ChromeType.CHROMIUM is working")
except:
    # run in local
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    print(f"driver is working")

wait = WebDriverWait(driver, 10)

data_list = []
df = pd.DataFrame()
page_count = 1

while True:
    print('page',page_count)
    try:
        total_data = driver.find_elements(By.CLASS_NAME, "kt-inbox__item")
        for i in range(len(total_data)):
            print(i)
            obat = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="inbox-list"]/div[{i+1}]/div[3]/div/span[1]')))
            obat.click()

            card = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="detailid"]')))

            # Find all elements with class 'form_field_caption'
            captions = card.find_elements(By.CLASS_NAME, "form-field-caption")

            # Find all elements with class 'form_field_input'
            inputs = card.find_elements(By.CLASS_NAME, "form-field-input")

            ori_data_dict = {}

            # Extract the values
            for caption_element, input_element in zip(captions, inputs):
                caption_value = caption_element.text.strip()

                input_div = input_element.find_element(By.XPATH, "./div")
                input_span = input_div.find_element(By.XPATH, "./span")
                input_value = input_span.text.strip()

                ori_data_dict[caption_value] = input_value

            # Preprocess the dictionary
            preprocessed_dict = {}
            current_key = None

            for key, value in ori_data_dict.items():
                # Remove '\n- -' from values
                value = value.replace('\n- -', '').replace(';','')
                # Replace a single dash '-' with None
                value = None if value.strip() == '-' else value.strip()

                if key == '':
                    # If the key is an empty string, combine the value with the previous key
                    if current_key is not None:
                        preprocessed_dict[current_key] += f' {value}' if value is not None else ''
                else:
                    # If the key is not an empty string, update the current key
                    current_key = key
                    preprocessed_dict[current_key] = value

            # Create a new dictionary with lowercase keys and underscores
            final_dict = {key.lower().replace(' ', '_'): value for key, value in preprocessed_dict.items()}

            print(final_dict)

            data_list.append(final_dict)

            # Close the pop-up
            close_button = driver.find_element(By.XPATH, "//*[@id='exampleModal2']/div/div/div[3]/button")
            close_button.click()


        # Save the data to a CSV file every 10 rows
        if data_list:
            df_temp = pd.DataFrame(data_list)
            df = pd.concat([df, df_temp], ignore_index=True)
            df_temp.to_csv(f'obat_bpom_page_{page_count}.csv', index=False)
            df.to_csv(f'obat.csv', index=False)
            data_list = []

        driver.execute_script("window.scrollTo(0, 0);")

        next_button = wait.until(EC.element_to_be_clickable((By.ID, "next")))
        next_button.click()
        wait.until(EC.staleness_of(next_button))

    except Exception as e:
        # Handle the exception when there is no "next" button or any other error
        print(f"An error occurred: {str(e)}")
        pass

    page_count += 1


# Close the WebDriver
driver.quit()


