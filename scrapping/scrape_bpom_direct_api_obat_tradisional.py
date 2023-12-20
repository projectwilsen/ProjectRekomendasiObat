import requests
import json
from bs4 import BeautifulSoup
import math
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
from dotenv import load_dotenv
import json

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_info(json.loads(SERVICE_ACCOUNT_FILE), scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = '14vUomCGwhSPZp8rBn3uGlUHbP-DU-x738_uJUjRsB2Q'
# SAMPLE_SPREADSHEET_ID = '19ksKPeIGr9yJVhD507SvtmKWN6UxSxZmx6Ei13IPZUQ'

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

data_list = []
offset = 4811

# for i in range(math.ceil(24703 / 10)):
for i in range(500):
    print(f'============= START PAGE {i+1} OFFSET {offset} ============= \n')

    url = 'https://cekbpom.pom.go.id/prev_next_pagination_obat_tradisional'

    data = {
        'offset': offset,
        'next_prev': offset + 9,
        'count_data_obat': 18414,
        'marked': 'next'
    }

    headers = {'X-Requested-With': 'XMLHttpRequest'}

    try:
        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 200:
            data = response.json()
            # print(data)
            for product_data in data['data_obat_tradisional']:
                # Extract 'PRODUCT_ID' and 'APPLICATION_ID'
                product_id = product_data.get('PRODUCT_ID', '')
                application_id = product_data.get('APPLICATION_ID', '')

                # print(product_id, application_id)

                url =  'https://cekbpom.pom.go.id/get_detail_produk_obat'
                data = {
                    'product_id' : product_id,
                    'aplication_id' : application_id
                }

                response = requests.post(url, data=data, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    rows = soup.find_all('tr')
                    # print(rows)
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
                    # print(final_dict)

                    data_list.append(final_dict)

                else:
                    print(f"No detail info: {response.status_code}")
        else:
            print(f"No info: {response.status_code}")
    except:
        pass

    if data_list:
        existing_header = sheet.values().get(spreadsheetId = SAMPLE_SPREADSHEET_ID, range = "bpom!A1:K1").execute()
        header_row = list(data_list[0].keys())

        if 'values' not in existing_header:
            values = [header_row]
            body = {'values': values}
            sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='bpom', valueInputOption='RAW', body=body).execute()
        elif existing_header['values'][0] != header_row:
            values = [header_row]
            body = {'values': values}
            sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='bpom!A1:Z1', valueInputOption='RAW', body=body).execute()


        values = []
        keys_to_handle = ['pendaftar_&_importir','diproduksi_oleh', 'pemberi_lisensi','pendaftar','pabrik','pemberi_kontrak',	'penerima_kontrak','pengemas_primer', 'pengemas_sekunder'] 

        for data in data_list:
            row_values = []

            for key in header_row:
                if key in keys_to_handle:
                    value = data.get(key, None)
                else:
                    value = data[key]

                row_values.append(value)

            values.append(row_values)



        # Append data rows
        body = {'values': values[1:]}
        sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='bpom', valueInputOption='RAW', body=body).execute()

        print(f"{len(data_list)} data appended successfully \n")

    offset += 10
    data_list = []