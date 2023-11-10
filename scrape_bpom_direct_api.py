import requests
import json
from bs4 import BeautifulSoup
import math
import pandas as pd

data_list = []
df = pd.DataFrame()
offset = 1

for i in range(math.ceil(24703 / 10)):
    print(f'============= PAGE {i+1} ============= \n')

    url = 'https://cekbpom.pom.go.id/prev_next_pagination_obat'

    data = {
        'offset': offset,
        'next_prev': offset + 9,
        'count_data_obat': 24703,
        'marked': 'next'
    }

    headers = {'X-Requested-With': 'XMLHttpRequest'}

    try:
        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 200:
            data = response.json()
            for product_data in data['data_obat']:
                # Extract 'PRODUCT_ID' and 'APPLICATION_ID'
                product_id = product_data.get('PRODUCT_ID', '')
                application_id = product_data.get('APPLICATION_ID', '')
                print(product_id, application_id)

                url =  'https://cekbpom.pom.go.id/get_detail_produk_obat'
                data = {
                    'product_id' : product_id,
                    'aplication_id' : application_id
                }

                response = requests.post(url, data=data, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    rows = soup.find_all('tr')
                    ori_data_dict = {}

                    for row in rows:
                        caption = row.find('td', class_='form-field-caption').find('b').text.strip()
                        input = row.find('td', class_='form-field-input').find('div').find('span').text.strip()
                        ori_data_dict[caption] = input
                
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

                    if data_list:
                        df_temp = pd.DataFrame(data_list)
                        df = pd.concat([df, df_temp], ignore_index=True)
                        # df_temp.to_csv(f'obat_bpom_page_{i+1}.csv', index=False)

                else:
                    print(f"No detail info: {response.status_code}")
        else:
            print(f"No info: {response.status_code}")
    except:
        pass

    offset += 10
    data_list = []

    print(f'============= DONE PAGE {i+1} ============= \n \n \n')

df.drop_duplicates(inplace = True)
df.to_csv(f'obat.csv', index=False)



